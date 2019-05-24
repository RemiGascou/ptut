# -*- coding: utf-8 -*-
"""
Genetion of random data sets
"""

import random

data = {
    "light":0,
    "sound":0,
    "temp" : {
        "object":0,
        "ambient":0
    }
}

def gen_data(fences, samples=100):
    """Documentation for new_function"""
    measures = []
    fence_light, fence_sound, fence_temp = fences

    olddata = {"light":int(random.random()*abs(fence_light["min"]-fence_light["max"])), "sound":int(random.random()*abs(fence_sound["min"]-fence_sound["max"])), "temp" : {"object":int(random.random()*abs(fence_temp["min"]-fence_temp["max"])), "ambient":int(random.random()*abs(fence_temp["min"]-fence_temp["max"]))}}
    data    = {"light":0, "sound":0, "temp" : {"object":0, "ambient":0}}

    fluct_scale = 10
    for k in range(samples):
        data    = {
            "light": max(min(fence_light["max"], olddata["light"]+(random.random()*fluct_scale-fluct_scale//2)), fence_light["min"]),
            "sound": max(min(fence_sound["max"], olddata["sound"]+(random.random()*fluct_scale-fluct_scale//2)), fence_sound["min"]),
            "temp" : {
                "object" : max(min(fence_temp["max"], olddata["temp"]["object"]+(random.random()*fluct_scale-fluct_scale//2)), fence_temp["min"]),
                "ambient": max(min(fence_temp["max"], olddata["temp"]["ambient"]+(random.random()*fluct_scale-fluct_scale//2)), fence_temp["min"])
            }
        }
        olddata = data
        measures.append(data)

    return measures


def gen_fence_fullscale() :
    fence_light = {"min":0, "max":1013}
    fence_sound = {"min":0, "max":1013}
    fence_temp  = {"min":0, "max":1013}
    return fence_light, fence_sound, fence_temp

def gen_fence_normal() :
    fence_light = {"min":10, "max":250}
    fence_sound = {"min":0, "max":85}
    fence_temp  = {"min":15, "max":35}
    return fence_light, fence_sound, fence_temp

def gen_fence_anomaly_001() :
    fence_light = {"min": 15, "max": 1013}
    fence_sound = {"min": 0,  "max": 100}
    fence_temp  = {"min": 15, "max": 1013}
    return fence_light, fence_sound, fence_temp

def gen_fence_anomaly_002() :
    fence_light = {"min":0, "max":400}
    fence_sound = {"min":0, "max":150}
    fence_temp  = {"min":0, "max":45}
    return fence_light, fence_sound, fence_temp

def gen_fence_anomaly_003() :
    fence_light = {"min":0, "max":1013}
    fence_sound = {"min":0, "max":1013}
    fence_temp  = {"min":0, "max":1013}
    return fence_light, fence_sound, fence_temp

def gen_fence_anomaly_004() :
    fence_light = {"min":0, "max":1000}
    fence_sound = {"min":0, "max":600}
    fence_temp  = {"min":0, "max":200}
    return fence_light, fence_sound, fence_temp

def gen_fence_normalsimple() :
    fence_light = {"min":0, "max":10}
    fence_sound = {"min":0, "max":10}
    fence_temp  = {"min":0, "max":10}
    return fence_light, fence_sound, fence_temp

def gen_fence_abnormalsimple() :
    fence_light = {"min":50, "max":60}
    fence_sound = {"min":50, "max":60}
    fence_temp  = {"min":50, "max":60}
    return fence_light, fence_sound, fence_temp


def genscenario(fileout, gfa, samples = 100):
    """Documentation for genscenario"""
    fences  = gfa()
    data    = gen_data(fences, samples)

    f = open(fileout, "w")
    for line in data:
        f.write(str(line).replace("\'", "\"")+"\n")
    f.close()
    return


if __name__ == '__main__':
    genscenario("data/50to60b.json", gen_fence_abnormalsimple,100)
    genscenario("data/norm1000.json", gen_fence_normal,1000)
    genscenario("data/ML_tests/anom1000.json", gen_fence_anomaly_002,1000)
