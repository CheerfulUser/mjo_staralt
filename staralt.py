#importing useful packages
import numpy as np
import matplotlib.pyplot as plt
#---
from astropy import units as u
from astropy.time import Time
#from astropy.table import Table
from astropy.coordinates import get_sun, get_moon, SkyCoord, EarthLocation, AltAz
#---
from astroplan import plots, observability_table
from astroplan import Observer, FixedTarget
from astroplan import AltitudeConstraint, AirmassConstraint, AtNightConstraint
from astroplan import is_observable, is_always_observable, months_observable
#---
import datetime


class Target():
	def __init__(self,ra, dec,date,name='target'):

		self._set_ra(ra)
		self._set_dec(dec)

		self._set_coord(date)
		self._set_fixed(name)
		self.name = name

	def _set_ra(self,ra):
		try:
			value = float(ra)
		except:
			value = ra
		self._ra = value

	def _set_dec(self,dec):
		try:
			value = float(dec)
		except:
			value = dec
		self._dec = value

	def _set_coord(self,date):
		if type(self._ra ) == str:
			c = SkyCoord(self._ra,self._dec, unit=(u.hourangle, u.deg),obstime=date.date)
		else:
			c = SkyCoord(self._ra,self._dec, unit=(u.deg, u.deg),obstime=date.date)
		self.coord = c 

	def _set_fixed(self,name):
		self.fixed_targ = FixedTarget(coord=self.coord,name=name)


class Observatory():
	def __init__(self,latitude = -43.29 * u.deg,longitude = 170.27 * u.deg,altitude = 1029 * u.m):
		self.lat = latitude
		self.long = longitude
		self.alt = altitude 
		self.obs_location = EarthLocation.from_geodetic(longitude, latitude, altitude)


class Date():
	def __init__(self,date=None):
		self._set_date(date)
		self._set_midnight()
		

	def _add_utc(self,time = None,add=True):
		if time is None:
			time = self.date.datetime
		if add:
			tmp = time+datetime.timedelta(hours=self.utc_offset)
		else:
			tmp = time+datetime.timedelta(hours=-self.utc_offset)
		return Time(tmp)

	def _set_date(self,date):
		if date is None:
			date = datetime.datetime.now(datetime.timezone.utc).astimezone()
			self.date = Time(date)
		else:
			self.date = Time(date)
		
		self.timezone = str(self.date.datetime.astimezone().tzinfo)
		self._set_utc_offset()
		self.date = self._add_utc()

	def _set_utc_offset(self):
		if self.timezone == 'NZDT':
			self.utc_offset = 13
		else:
			self.utc_offset = 12

	def _set_midnight(self):
		midnight = str((self.date.datetime+datetime.timedelta(days=1)).strftime('%Y-%m-%d')+'T'+'00:00:00')   
		self.midnight = self._add_utc(time = Time(midnight).datetime,add = False)


class Altitudes():
	def __init__(self,observatory,date,target):
		self._set_time(date)
		self._set_atazframe(observatory)
		self._get_sun_moon()
		self._transform_target(target)
		self.targ_name = target.name

	def _set_time(self,date):
		delta_midnight = np.arange(-12, 12, .1) * u.hour 
		self.time = date.midnight + delta_midnight
		self.x_time = delta_midnight

	def _set_atazframe(self,observatory):
		altazframe = AltAz(obstime=self.time, location=observatory.obs_location)
		self.altazframe = altazframe
	
	def _get_sun_moon(self):
		self.sun = get_sun(self.time).transform_to(self.altazframe)
		self.moon = get_moon(self.time).transform_to(self.altazframe)

	def _transform_target(self,target):
		self.target = target.coord.transform_to(self.altazframe)


class Visibility():
	def __init__(self,altitudes,date,plot=True):

		if plot:
			self.plot(altitudes, date)


	def plot(self,altitudes,date):
		zeroLine_x1=np.arange(-12,90,10)
		zeroLine_y1=np.full(len(zeroLine_x1),30)
		zeroLine_y2=np.full(len(zeroLine_x1),40)

		plt.figure(figsize=(10,5))
		plt.plot(zeroLine_x1,zeroLine_y1,"-",linewidth=7,color="red",label="limiting altitude")
		plt.plot(zeroLine_x1,zeroLine_y2,"-",linewidth=2,color="red",label="warning altitude")
		plt.plot(altitudes.x_time, altitudes.moon.alt, color=[0.75]*3, ls='--', label='Moon')

		# plotting the alitudes of the objects
		plt.plot(altitudes.x_time,altitudes.target.alt,label=altitudes.targ_name) 

		# defining twilight/nighttimes
		# plt.fill_between(delta_midnight, 0, 90, sunaltazs.alt < -0*u.deg, color='0.5', zorder=0)  
		# plt.fill_between(delta_midnight, 0, 90, sunaltazs.alt < -18*u.deg, color='k', zorder=0)   
		plt.fill_between(altitudes.x_time, 0, 90, altitudes.sun.alt < -0*u.deg, color='sandybrown', zorder=0, alpha = 0.2)  
		plt.fill_between(altitudes.x_time, 0, 90, altitudes.sun.alt < -6*u.deg, color='cornflowerblue', zorder=0, alpha = 0.2) 
		plt.fill_between(altitudes.x_time, 0, 90, altitudes.sun.alt < -12*u.deg, color='darkblue', zorder=0, alpha = 0.2)  
		plt.fill_between(altitudes.x_time, 0, 90, altitudes.sun.alt < -18*u.deg, color='k', zorder=0, alpha = 0.2)  

		plt.legend()
		plt.xlim(-4.5, 8)          #can change this as appropriate, it is the number of hours before and after midnight (ie on your x-axis)
		plt.ylim(0, 90)  #could range from 0-90 degrees
		plt.xlabel('Hours from Midnight',fontsize=15)  
		plt.ylabel('Altitude [deg]',fontsize=15)  
		plt.title("Object Visibility on {}".format(date.date.datetime.strftime('%d-%m-%Y')),fontsize=15)
		plt.grid()
		#plt.savefig('TargetVisibility_{}.png'.format(obs_dates_save))
		print('figure')
		plt.show(block=True)