import pandas as pd
import numpy as np
import random as rnd
import matplotlib.pyplot as plt
from scipy import stats

class GregUtils():

    def __init__(self):
        return

    def make_ref_plot(self):
        plt.subplots(2,1,figsize=(10,2.5),dpi=100)

        plt.subplot(1,2,1)
        plt.hist(self.long_run, color='navy', label="Historical")
        x_lim=(self.lr_mu-3*self.lr_sig,self.lr_mu+3*self.lr_sig)
        plt.xlim(x_lim)
        plt.legend(loc='best')

        plt.subplot(1,2,2)
        plt.hist(self.short_run, color='red', alpha=0.75,label="Current")
        plt.xlim(x_lim)

        plt.legend(loc='best')
        plt.show()
        print('')
        return

    def make_estimate(self):

        p_value=stats.ttest_ind(self.short_run, self.long_run,
                axis=0, equal_var=True)[1]

        print(f"\nP_value is approximately {p_value:0.4f}\n")

        if p_value < self.target_p:
            print(f"We can not assume that the difference in means is just random, and must ")
            print("assume that the mean of the sample is representative of this run's mean")
            print("production time.  Assume that the next {self.hours} hours")
            print(f"will produce {60*self.hours/np.mean(self.short_run):.0f} parts")

        else:
            print(f"We assume that the difference in means is just random, and must ")
            print("assume that the mean of the history is representative of this run's")
            print("eventual mean production time.  Assume that the next {self.hours} hours")
            print(f"will produce {60*self.hours/np.mean(self.long_run):.0f} parts")

        return

    def show_test_case(self,lr_mu=5,lr_sig=0.5,sr_mu=4.9,sr_sig=0.5,
                lr_num_sam=3000,sr_num_sam=20,
                target_p = 0.05,hours = 24):

        self.long_run=np.random.normal(lr_mu, lr_sig,lr_num_sam)
        self.short_run=np.random.normal(sr_mu, sr_sig,sr_num_sam)
        self.lr_mu = lr_mu
        self.lr_sig = lr_sig
        self.sr_mu = sr_mu
        self.sr_sig = sr_sig
        self.lr_num_sam = lr_num_sam
        self.sr_num_sam = sr_num_sam
        self.target_p = target_p
        self.hours = hours

        indy=['# Samples','Mean','Sdev']

        df=pd.DataFrame(index=indy)
        df['History'] = [self.lr_num_sam,round(np.mean(self.long_run),2),round(np.std(self.long_run),2)]
        df['Current Lot'] = [self.sr_num_sam,round(np.mean(self.short_run),2),round(np.std(self.short_run),2)]

        self.make_ref_plot()
        print(df)
        self.make_estimate()

        return
