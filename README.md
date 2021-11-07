# F1 Analysis Suite
### A Set Of Tools To Analyse F1 Sessions, Powered By The Fast F1 Library

## Modes

<details>
  <summary>Fastest Technically Possible Lap Time</summary>
  
This Tool Works By Going Through A Drivers Mini Sectors Of Every Lap And Finds The Fastest Ones. These Are Then Added Together To Produce The Fastest Technically Possible Lap Time. This Obviously Completely Ignores Tyre Wear, Tyre Temp, Fuel Load, Slipstream And Dirty Air. This Time Is Near Impossible To Actually Achieve But Is A Fun Metric To Know.

This Tool Is Run By Using The Mode `FTPLT`

Requires:
- `driver` - Drivers Three Letter Identifier (E.G. NOR)
- `-y` `--year` - Year The Session Took Place (E.G. 2021)
- `-r` `--race` - The Race Weekends Number (E.G. 10 (Austria))
- `-s` `--session` - The Session Name (E.G. R, SQ, Q, FP3, FP2, FP1)

Optional:
- `-m` `--minisectors` - The Amount Of Mini Sectors To Analyse, Defaults To 25
- `-v` `--verbose` - Adds More Output Data

Example Run Code: `python main.py FTPLT NOR -y 2021 -r 9 -s R -v`

Which Outputs:
```Python Console
core           INFO     Loading laps for Austrian Grand Prix - Race [v2.1.8]
api            INFO     Using cached data for timing_data
api            INFO     Using cached data for timing_app_data
core           INFO     Processing timing data...
api            INFO     Using cached data for session_status_data
api            INFO     Using cached data for track_status_data
api            INFO     Using cached data for car_data
api            INFO     Using cached data for position_data
api            INFO     Using cached data for weather_data
core           INFO     Loaded data for 19 drivers: ['14', '3', '16', '5', '77', '44', '4', '47', '9', '22', '63', '18', '33', '6', '99', '11', '7', '55', '10']
                     Fastest Technically Possible MiniSectors

  MiniSector         Speed                 Gear                ~Time          Lap
 ─────────────────────────────────────────────────────────────────────────────────
      1        298.09090909090907   7.818181818181818    2.0780290210430015   53
      2        315.5882352941176           8.0           1.9628157539608582   53
      3        247.52173913043478   6.6521739130434785   2.502574368522748    42
      4        221.2173913043478    5.043478260869565    2.8001485613207557    1
      5              270.0          6.7368421052631575   2.2942280000000004    1
      6        295.8421052631579    7.631578947368421    2.0938248781355635   53
      7        316.47058823529414          8.0           1.9573432193308553   53
      8        300.8333333333333           8.0           2.0590855180055407   21
      9        138.57894736842104          3.0           4.469954287884544     1
      10             249.95                6.0           2.4782618923784763    1
      11       285.6111111111111    7.277777777777778    2.168828648122934    53
      12       317.1764705882353           8.0           1.952987114243324    53
      13       254.52380952380952   6.714285714285714    2.433727363891488     4
      14       194.69230769230768   4.230769230769231    3.1816437297510873    1
      15       249.8695652173913           6.0           2.479059662432574     1
      16       247.95454545454547          6.0           2.498206108157654    67
      17       215.95833333333334   5.208333333333333    2.8683383060003864    1
      18             233.0          5.695652173913044    2.6585474678111596   62
      19       244.13636363636363   5.7727272727272725   2.537276916775275     1
      20             265.35                6.65          2.3344321085358963   55
      21       288.6842105263158           7.0           2.145741046490429    55
      22       293.57894736842104          7.0           2.1099658730727864   64
      23       245.63636363636363   6.136363636363637    2.521782812731311    57
      24       199.15384615384616   4.423076923076923    3.1103670451911944   30
      25       255.09677419354838   6.225806451612903    2.4282610470409716   56

Fastest Technically Possible Lap Time ~0:01:02.125431
Actual Fastest Lap 0:01:08.471000 On Lap 62.0
Fastest Technically Possible Time Made Up From MiniSectors On Laps: [53.0, 42.0, 1.0, 21.0, 4.0,
67.0, 62.0, 55.0, 64.0, 57.0, 30.0, 56.0]
Differance In Lap Times: 0:00:06.345569
core           INFO     Loading laps for Austrian Grand Prix - Race [v2.1.8]
api            INFO     Using cached data for timing_data
api            INFO     Using cached data for timing_app_data
core           INFO     Processing timing data...
api            INFO     Using cached data for session_status_data
api            INFO     Using cached data for track_status_data
api            INFO     Using cached data for car_data
api            INFO     Using cached data for position_data
api            INFO     Using cached data for weather_data
core           INFO     Loaded data for 19 drivers: ['14', '3', '16', '5', '77', '44', '4', '47', '9', '22', '63', '18', '33', '6', '99', '11', '7', '55', '10']
 Actual Fastest Lap Vs Fastest Technically
                Possible Lap

  MiniSector   Gain/Loss   Time Differance
 ──────────────────────────────────────────
      1          Lost      0:00:00.093926
      2          Lost      0:00:00.120999
      3          Lost      0:00:00.154982
      4          Lost      0:00:00.979029
      5          Lost      0:00:00.152316
      6          Lost      0:00:00.074049
      7          Lost      0:00:00.132227
      8          Lost      0:00:00.101624
      9          Lost      0:00:01.311655
      10         Lost      0:00:00.527613
      11         Lost      0:00:00.120045
      12         Lost      0:00:00.153580
      13        Gained     0:00:00.011781
      14         Lost      0:00:01.571408
      15         Lost      0:00:00.193952
      16         Lost      0:00:00.010538
      17         Lost      0:00:00.368759
      18        Gained     0:00:00.010377
      19         Lost      0:00:00.300802
      20         Lost      0:00:00.034154
      21         Lost      0:00:00.023732
      22         Lost      0:00:00.005689
      23         Lost      0:00:00.028359
      24        Gained     0:00:00.017741
      25         Lost      0:00:00.072156
```
</details>

<details>
  <summary>Fastest Lap Mini Sectors</summary>
  
This Tool Works By Getting A Drivers Mini Sectors From Their Fastest Lap. This Then Outputs The Average Speed And Gear Of The Mini Sector, And The Rough Time It Took To Pass Through It.

This Tool Is Run By Using The Mode `FLMS`

Requires:
- `driver` - Drivers Three Letter Identifier (E.G. NOR)
- `-y` `--year` - Year The Session Took Place (E.G. 2021)
- `-r` `--race` - The Race Weekends Number (E.G. 10 (Austria))
- `-s` `--session` - The Session Name (E.G. R, SQ, Q, FP3, FP2, FP1)

Optional:
- `-m` `--minisectors` - The Amount Of Mini Sectors To Analyse, Defaults To 25
- `returnMode` - Only Used Internally By Other Scripts But Allows Them To Take The Data As Pandas DataFrame

Example Run Code: `python main.py FLMS NOR -y 2021 -r 9 -s R -v`

Which Outputs:
```Python Console
core           INFO     Loading laps for Austrian Grand Prix - Race [v2.1.8]
api            INFO     Using cached data for timing_data
api            INFO     Using cached data for timing_app_data
core           INFO     Processing timing data...
api            INFO     Using cached data for session_status_data
api            INFO     Using cached data for track_status_data
api            INFO     Using cached data for car_data
api            INFO     Using cached data for position_data
api            INFO     Using cached data for weather_data
core           INFO     Loaded data for 19 drivers: ['3', '11', '7', '77', '22', '33', '5', '18', '16', '63', '6', '4', '55', '10', '44', '99', '14', '9', '47']
                           Fastest Lap MiniSectors

  MiniSector         Speed                 Gear                ~Time
 ───────────────────────────────────────────────────────────────────────────
      1              285.2                 7.0           2.166059887798037
      2        297.2631578947368           7.0           2.078159582152975
      3        233.08695652173913   6.565217391304348    2.6503425554933786
      4        163.9090909090909    4.181818181818182    3.7689201774819754
      5        253.1904761904762    6.142857142857143    2.439903306375776
      6        285.7368421052632           7.0           2.161990296555535
      7        296.44444444444446          7.0           2.083898995502249
      8        286.6842105263158           7.0           2.154845845419498
      9              107.14                3.06          5.765916371103231
      10       206.07692307692307   4.653846153846154    2.997716924225458
      11       270.63157894736844   6.7368421052631575   2.2826614780241155
      12       294.05263157894734          7.0           2.1008493502774304
      13       255.76190476190476   6.904761904761905    2.4153725339787755
      14            130.325               3.375           4.74015177441013
      15       231.7391304347826    5.521739130434782    2.665757305816136
      16       246.91304347826087   5.739130434782608    2.501934572988203
      17       191.35714285714286          5.0           3.2283105337812623
      18       233.91304347826087   5.739130434782608    2.6409826096654276
      19       218.2608695652174    5.3478260869565215   2.830375784860558
      20       261.5238095238095    6.571428571428571    2.362156933721778
      21       285.5263157894737           7.0           2.1635843907834102
      22       292.7894736842105           7.0           2.1099128743483737
      23       242.9047619047619    6.095238095238095    2.543220129386395
      24       200.2962962962963    4.777777777777778    3.084232167159764
      25       247.73529411764707   6.029411764705882    2.493630478451858
```
</details>

<details>
  <summary>Predicted Race Position</summary>
  
This Tool Works By Getting Every Race Start & End Positions From An Inputted Driver Works Out The Most Common Result, And It's % Of Happening. Drivers With Larger Data Sets E.G. Räikkönen or Alonso Have The Highest Chance Of Being Close To The Actual Result Compared To A Rookie Like Mick Schumacher.

This Tool Is Run By Using The Mode `PRP`

Requires:
- `driver` - Drivers Three Letter Identifier (E.G. HAM)
- `-sp` `--startingpos` - The Drivers Starting Pos (E.G. 1)

Optional:
- `-v` `--verbose` - Adds More Output Data

Example Run Code: `python main.py PRP HAM -sp 1 -v`

Which Outputs:
```Python Console
Race Start To Race End                          
       Positions                                
                                                
  Start Pos   End Pos                           
 ─────────────────────                          
      1          1                              
      1          1                              
      1          3                              
      1          1                              
      1          1                              
      1          1                              
      1          1                              
      1          5                              
      1          3                              
      1         12                              
      1          1                              
      1          2                              
      1          1                              
      1          1                              
      1          2                              
      1          3                              
      1          3                              
      1          1                              
      1          1                              
      1          3                              
      1          4                              
      1          5                              
      1          1                              
      1          3                              
      1          1                              
      1          1                              
      1          1                              
      1          1                              
      1          1                              
      1          1                              
      1          1                              
      1          2                              
      1          1                              
      1          1                              
      1          3                              
      1          1                              
      1          2                              
      1          1                              
      1          6                              
      1          1                              
      1          1                              
      1          2                              
      1          3                              
      1          1                              
      1          1                              
      1          1                              
      1          2                              
      1          1                              
      1          1                              
      1          1                              
      1          1                              
      1          2                              
      1          1                              
      1          1                              
      1          1                              
      1          5                              
      1          1                              
      1          1                              
      1          1                              
      1          2                              
      1          1                              
      1          1                              
      1          2                              
      1          1                              
      1          1                              
      1          2                              
      1          1                              
      1          2                              
      1          1                              
      1          1                              
      1          3                              
      1          1                              
      1          1                              
      1          2                              
      1          1                              
      1          1                              
      1          9                              
      1          1                              
      1          1                              
      1          1                              
      1          1                              
      1          1                              
      1          1                              
      1          7                              
      1          1                              
      1          3                              
      1          1                              
      1          1                              
      1          2                              
      1          1                              
      1          2                              
                                                
Most Likely Finishing Place Is 1.               
With A 65% Chance.                              
```
</details>