#!/usr/bin/env python
import ROOT
import re
from array import array
import sys
import csv
from math import sqrt
from math import pi
import datetime
import argparse
# from sys import path
# path.append("../../../MacrosAndScripts/")
# from myPlotStyle import *
ROOT.gStyle.SetFrameLineWidth(1)
ROOT.gStyle.SetLineWidth(2)
ROOT.gStyle.SetOptStat(0)
#mc_samples = [ 'EWKWMinus', 'EWKWPlus', 'EWKZ2Jets', 'GluGluH', 'GluGluZH', 'ST_t', 'VBFH', 'VV', 'VVV', 'WplusH', 'WminusH', 'ZH', 'ZJetsToNuNu']
mc_dict = {'STT': ['ST_t'] ,
           'VVT': ['VV', 'VVV' ],
           'otherMC' : [ 'EWKWMinus', 'EWKWPlus', 'EWKZ2Jets', 'GluGluH', 'GluGluZH' , 'VBFH', 'WplusH', 'WminusH', 'ZH', 'ZJetsToNuNu' ]
       }
final_mc_list=['ZTTjet', 'ZLLjet', 'TT']
        
def checkHistogram(f, histogram):
    isthere=  f.GetListOfKeys().Contains(histogram)
    #print(isthere)
    return isthere


def GetKeyNames( self, dir = "" ):
    self.cd(dir)
    return [key.GetName() for key in ROOT.gDirectory.GetListOfKeys()]
ROOT.TFile.GetKeyNames = GetKeyNames


def getHistList_v3(inFile):
    keyList = inFile.GetKeyNames()
    tmpList= []
    for tdir in keyList:
        print 'tdir  =  ', tdir
        for key, value in mc_dict.items():
            print key, value
            mc_samples = value
            smallMC = inFile.Get(tdir+'/'+mc_samples[0]+'_'+tdir).Clone()
            smallMC.Reset("ICES")
            for mc in mc_samples:
                tmppath = tdir+'/'+mc+'_'+tdir
                #print 'path  =  ', tmppath
                try:
                    tmpHist = inFile.Get(tmppath)
                    #print 'intergal = ', tmpHist.Integral()
                    smallMC.Add(tmpHist)
                except:
                    pass
            #print 'integral  otherMC', otherMC.Integral()
            inFile.cd(tdir)
            smallMC.SetName(key+"_"+tdir)
            smallMC.Write()
    return 

    
def main(histogram):
    inFile_nominal= ROOT.TFile("f_"+histogram+"_initial.root","UPDATE")
    inFile_up     = ROOT.TFile("f_"+histogram+"_up.root","UPDATE")
    inFile_down   = ROOT.TFile("f_"+histogram+"_down.root","UPDATE")
    getHistList_v3(inFile_nominal)
    inFile_nominal.Close()
    getHistList_v3(inFile_up)
    inFile_up.Close()
    getHistList_v3(inFile_down)
    inFile_down.Close()


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--hist",
                    help="name of histogram elePt , tauPt, ..  Default=etau")
    args =  parser.parse_args()
    if args.hist is None:
        histogram = 'etau'
    else:
        histogram = args.hist
    print 'histogram = ' , histogram
    main(histogram)

