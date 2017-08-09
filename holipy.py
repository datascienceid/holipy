import pandas as pd
import numpy as np
import Levenshtein as L

# dh=pd.read_csv('Holiday.csv')
dh=pd.read_pickle('data_h')

def rat_l(x,y):
	X=x.split(' ')
	Y=y.split(' ')
	rr=0
	for m in X:
		for n in Y:
			if rr<=L.ratio(m.lower(),str(n.lower())):
				rr=L.ratio(m.lower(),str(n.lower()))
	return rr

def auto_complete_hol(nl):
	bn=dh.HoliDay.unique().tolist()
	en=dh.HoliDay_E.unique().tolist()
	real_bn=[]
	real_en=[]
	for n in nl:
		if type(n)!=str:
				pass
				print 'WARNING some names is not a string'
		else:
			for def_en,def_bn in zip(en,bn):
				if rat_l(n,def_bn)>=0.78:
					real_bn.append(def_bn)

				if rat_l(n,def_en)>=0.78:
					real_en.append(def_en)

	if len(set(real_bn)|set(real_en))<len(nl):
		print "WARNING some names is not on the database"

	return real_bn,real_en

class holi_id():
	def __init__(self,lang='Bahasa'):
		self.average_holiday_per_year=float(len(dh))/len(dh.year_holiday.unique().tolist())
		self.average_holiday_per_month=float(len(dh))/(len(dh.year_holiday.unique().tolist())*len(dh.month_holiday.unique().tolist()))
		self.range_date=str(min(dh.year_holiday))+'_'+str(min(dh.month_holiday))+'-'+str(max(dh.year_holiday))+'_'+str(max(dh.month_holiday))
		if lang.lower()=='english':
			self.name_holiday=dh.HoliDay_E.unique().tolist()
			self.language='English'
		elif lang.lower()=='bahasa':
			self.language='Bahasa'
			self.name_holiday=dh.HoliDay.unique().tolist()
		else:
			print "WARNING language is filled by 'English' or 'Bahasa'. The program still run with default setting"
			self.name_holiday=dh.HoliDay.unique().tolist()

	def on_date(self, year=None, month=None, name_holiday=True,lang='Bahasa'):
		e1=''

		if year==None:
			y=[2015+i for i in range(3)]
			if month==None:
				m=dh[dh.year_holiday.isin(y)].month_holiday.unique().tolist()
			elif type(month)!=list:
				e1='ERROR month must list with integer between 1-12'
			else:
				m=month
		elif type(year)!=list:
			e1='ERROR year must list with integer between 2013-2018'
		else:
			y=year
			if month==None:
				m=dh[dh.year_holiday.isin(y)].month_holiday.unique().tolist()
			elif type(month)!=list:
				e1='ERROR month must list with integer between 1-12'
			else:
				m=month

		if e1!='':
			print e1
		else:
			dh2=dh[(dh.year_holiday.isin(y))&(dh.month_holiday.isin(m))]
			if name_holiday==0:
				self.the_holiday=dh2[['date_holiday']]
			else:
				if lang.lower()=='english':
					self.language='English'
					self.name_holiday=dh2.HoliDay_E.unique().tolist()
					self.the_holiday=dh2[['HoliDay_E','date_holiday']]
				elif lang.lower()=='bahasa':
					self.language='Bahasa'
					self.name_holiday=dh2.HoliDay.unique().tolist()
					self.the_holiday=dh2[['HoliDay','date_holiday']]
				else:
					print "WARNING language is filled by 'English' or 'Bahasa'. The program still run with first setting"
					if self.language=='English':
						self.name_holiday=dh2.HoliDay_E.unique().tolist()
					else :
						self.name_holiday=dh2.HoliDay.unique().tolist()	

			self.the_holiday_date=dh2[['year_holiday','month_holiday']]
			self.range_date=str(min(self.the_holiday_date.year_holiday))+'_'+str(min(self.the_holiday_date.month_holiday))+'-'+str(max(self.the_holiday_date.year_holiday))+'_'+str(max(self.the_holiday_date.month_holiday))



			self.average_holiday_per_year=float(len(dh2))/len(dh2.year_holiday.unique().tolist())
			self.average_holiday_per_month=float(len(dh2))/(len(dh2.year_holiday.unique().tolist())*len(dh2.month_holiday.unique().tolist()))

	def on_holiday_name(self, name=None, name_holiday=True,lang='Bahasa'):
		e1=''
		if name==None:
			y=[2015+i for i in range(3)]
			na=dh[dh.year_holiday.isin(y)].holiDay.unique().tolist()
		else:
			na=name.split(',')

		na2_bn,na2_en=auto_complete_hol(na)
		dh2=dh[(dh.HoliDay.isin(na2_bn))|(dh.HoliDay_E.isin(na2_en))]
		if name_holiday==0:
			self.the_holiday=dh2[['date_holiday']]
		else:
			if lang.lower()=='english':
				self.language='English'
				self.name_holiday=dh2.HoliDay_E.unique().tolist()
				self.the_holiday=dh2[['HoliDay_E','date_holiday']]
			elif lang.lower()=='bahasa':
				self.language='Bahasa'
				self.name_holiday=dh2.HoliDay.unique().tolist()
				self.the_holiday=dh2[['HoliDay','date_holiday']]
			else:
				print "WARNING language is filled by 'English' or 'Bahasa'. The program still run with first setting"
				if self.language=='English':
					self.name_holiday=dh2.HoliDay_E.unique().tolist()
				else :
					self.name_holiday=dh2.HoliDay.unique().tolist()

		self.the_holiday_date=dh2[['year_holiday','month_holiday']]
		self.range_date=np.nan
		self.average_holiday_per_year=np.nan
		self.average_holiday_per_month=np.nan