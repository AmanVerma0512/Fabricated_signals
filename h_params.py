header={
    "subScores":True,
    "coachingTip":True,
    "score":True,
    "meta":True
}

h_params1={
                        "global_score": 25,
                        "setting":"experiment",
                         "bwt": 60,
                         "gender": "men's",
                         "exercise_mode": "Equipped Powerlifting",
                         "l0": 1,
                         "l1": 1,
                         "l2": 1,
                         "l3": 1,
                         "power":{
                             "w_power": 1,
                             "w_explosiveness": 1,
                              "peaks": {
                                  "sz": 12,
                                  "max_win": 100
                              },

                              "mode": {
                                  "sz": 12
                              },
                            "power":{
                                "growth factor":1.15,
                                 "bwt": 60,
                                 "gender": "men's",
                                 "exercise_mode": "Equipped Powerlifting",
                                 "scipyPeaks":False,
                                 "intervalPeaks":None
                                 # "peaks": {
                                 #     "sz": 12,
                                 #     "max_win": 100
                                 # },
                             },
                             "explosiveness":{
                                 "scipyPeaks":False,
                                 "intervalPeaks":None
                                 # "peaks": {
                                 #     "sz": 12,
                                 #     "max_win": 100
                                 # },
                             }
                         },

                         "formScore":{
                            "w_jitter": 1,
                            "w_tempo": 1,
                            "w_sudden release": 1,
                            "sudden release": {
                                "max_to_fall_ratio": 0.4,
                                "fall_time": 4
                            },
                            "tempo":{
                                "scipyPeaks":False,
                                "intervalPeaks":False
                            },
                            "peaks": {
                                "sz": 12,
                                "max_win": 100
                            },
                            "jitter": {
                                "window_size": 4,
                                "delta": 2,
                                "t0": 2,
                                "x_dist_rel": 0.2,
                                "jitterPolicyThreshold":4,
                                "scipyPeaks":False,

                                # "smoothBlips": {
                                #     "smoothenFactor": 2,
                                #     "prominentPeaksProminence":0.5,
                                #     "prominentPeaksWidth":2,
                                #     "smallPeaksHeightLowerFactor":0.6,
                                #     "smallPeaksHeightHigherFactor":0.8,
                                #     "smallPeaksWidth":2
                                # }
                            },

                            "peaks": {
                                "sz": 12,
                                "max_win": 100
                            },

                            "mode": {
                                "sz": 12
                            },
                         },

                         "stamina":{
                            "w_ring stamina": 1,
                            "w_area stamina": 1,
                            "w_total time":1,
                            "peaks": {
                                "scipyPeaks":False,
                                "intervalPeaks":None,
                                "sz": 12,
                                "max_win": 100
                            },
                            "area stamina":
                            {
                                "referenceFactor":1.4,
                                "peaks":{
                                "scipyPeaks":False,
                                "intervalPeaks":None
                                # "peaks": {
                                #     "sz": 12,
                                #     "max_win": 100
                                # },
                                }
                            },
                            "total time":
                            {
                                "referenceFactor":1.4,
                                "peaks":{
                                "scipyPeaks":False,
                                "intervalPeaks":None
                                # "peaks": {
                                #     "sz": 12,
                                #     "max_win": 100
                                # },
                                }
                            },
                            "ring stamina":{
                                "baseBased":False,
                                "peakBased":{
                                    "power_ref":0.8,
                                    "time_ref":200
                                }
                            },
                            "peaks":{
                                 "scipyPeaks":False,
                                 "intervalPeaks":None
                                 # "peaks": {
                                 #     "sz": 12,
                                 #     "max_win": 100
                                 # },
                                 },
                             "mode": {
                                 "sz": 12
                             },
                         },

                         "discount": 0.9,
                         "peaks": {
                             "sz": 12,
                             "max_win": 100
                         },

                         "mode": {
                             "sz": 12
                         },

                         "print": 0,
                         "plot": 0,
                         "log_dir": "D:/Forge/Forge/jupyter/formscore-log/",
                         }


h_params={
                        "global_score": 25,
                        "setting":"experiment",
                         "bwt": 60,
                         "gender": "men's",
                         "exercise_mode": "Equipped Powerlifting",
                         "l0": 1,
                         "l1": 1,
                         "l2": 1,
                         "l3": 1,
                         "power":{
                             "w_power": 1,
                             "w_explosiveness": 1,
                              "peaks": {
                                  "sz": 12,
                                  "max_win": 100
                              },

                              "mode": {
                                  "sz": 12
                              },
                            "power":{
                                "growth factor":1.15,
                                 "bwt": 60,
                                 "gender": "men's",
                                 "exercise_mode": "Equipped Powerlifting",
                                 "scipyPeaks":False,
                                 "intervalPeaks":None
                                 # "peaks": {
                                 #     "sz": 12,
                                 #     "max_win": 100
                                 # },
                             },
                             "explosiveness":{
                                 "scipyPeaks":False,
                                 "intervalPeaks":None
                                 # "peaks": {
                                 #     "sz": 12,
                                 #     "max_win": 100
                                 # },
                             }
                         },

                         "formScore":{
                            "w_jitter": 1,
                            "w_tempo": 1,
                            "w_sudden release": 1,
                            "sudden release": {
                                "max_to_fall_ratio": 0.4,
                                "fall_time": 4
                            },
                            "tempo":{
                                "scipyPeaks":False,
                                "intervalPeaks":False
                            },
                            "peaks": {
                                "sz": 12,
                                "max_win": 100
                            },
                            "jitter": {
                                "window_size": 4,
                                "delta": 2,
                                "t0": 2,
                                "x_dist_rel": 0.2,
                                "jitterPolicyThreshold":4,
                                "scipyPeaks":False,

                                # "smoothBlips": {
                                #     "smoothenFactor": 2,
                                #     "prominentPeaksProminence":0.5,
                                #     "prominentPeaksWidth":2,
                                #     "smallPeaksHeightLowerFactor":0.6,
                                #     "smallPeaksHeightHigherFactor":0.8,
                                #     "smallPeaksWidth":2
                                # }
                            },

                            "peaks": {
                                "sz": 12,
                                "max_win": 100
                            },

                            "mode": {
                                "sz": 12
                            },
                         },

                         "stamina":{
                            "w_ring stamina": 1,
                            "w_area stamina": 1,
                            "w_total time":1,
                            "peaks": {
                                "scipyPeaks":False,
                                "intervalPeaks":None,
                                "sz": 12,
                                "max_win": 100
                            },
                            "area stamina":
                            {
                                "referenceFactor":1.4,
                                "peaks":{
                                "scipyPeaks":False,
                                "intervalPeaks":None
                                # "peaks": {
                                #     "sz": 12,
                                #     "max_win": 100
                                # },
                                }
                            },
                            "total time":
                            {
                                "referenceFactor":1.4,
                                "peaks":{
                                "scipyPeaks":False,
                                "intervalPeaks":None
                                # "peaks": {
                                #     "sz": 12,
                                #     "max_win": 100
                                # },
                                }
                            },
                            "ring stamina":{
                                "baseBased":False,
                                "peakBased":{
                                    "power_ref":0.8,
                                    "time_ref":200
                                }
                            },
                            "peaks":{
                                 "scipyPeaks":False,
                                 "intervalPeaks":None
                                 # "peaks": {
                                 #     "sz": 12,
                                 #     "max_win": 100
                                 # },
                                 },
                             "mode": {
                                 "sz": 12
                             },
                         },

                         "discount": 0.9,
                         "peaks": {
                             "sz": 12,
                             "max_win": 100
                         },

                         "mode": {
                             "sz": 12
                         },

                         "print": 0,
                         "plot": 0,
                         "log_dir": "D:/Forge/Forge/jupyter/formscore-log/",
                         }




y=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 12, 14, 15, 17, 17, 16, 14, 15, 15, 14, 14, 13, 14, 11, 10, 10, 10, 10,
                       10, 10, 10, 10, 10, 10, 0, 10, 0, 10, 13, 14, 16, 17, 17, 15, 15, 14, 13, 14, 13, 12, 11, 10, 10,
                       10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11, 10, 12, 13, 16, 17, 17, 16, 15, 15, 13, 13, 12, 12,
                       11, 10, 10, 11, 10, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 10, 0, 11, 15, 16, 16, 16, 16, 16,
                       15, 12, 12, 12, 11, 11, 10, 10, 0, 11, 11, 10, 11, 10, 0, 10, 11, 12, 11, 12, 11, 0, 12, 17, 17,
                       17, 17, 15, 12, 11, 12, 11, 10, 10, 11, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11, 10, 0, 10, 15,
                       17, 16, 17, 15, 14, 13, 13, 12, 11, 11, 11, 11, 10, 10, 11, 10, 10, 0, 10, 11, 11, 10, 10, 11,
                       10, 10, 10, 0, 10, 16, 16, 16, 15, 16, 16, 14, 13, 12, 11, 11, 11, 11, 10, 10, 10, 10, 10, 10,
                       10, 10, 10, 11, 10, 11, 10, 11, 10, 0, 10, 14, 16, 16, 17, 16, 16, 15, 14, 13, 12, 12, 11, 10,
                       11, 11, 11, 11, 10, 10, 11, 10, 11, 10, 10, 11, 10, 10, 11, 11, 0]
