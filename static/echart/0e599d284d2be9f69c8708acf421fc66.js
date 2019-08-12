(function (root, factory) {if (typeof define === 'function' && define.amd) {define(['exports', 'echarts'], factory);} else if (typeof exports === 'object' && typeof exports.nodeName !== 'string') {factory(exports, require('echarts'));} else {factory({}, root.echarts);}}(this, function (exports, echarts) {var log = function (msg) {if (typeof console !== 'undefined') {console && console.error && console.error(msg);}};if (!echarts) {log('ECharts is not Loaded');return;}if (!echarts.registerMap) {log('ECharts Map is not loaded');return;}echarts.registerMap('普兰县', {"type":"FeatureCollection","features":[{"type":"Feature","id":"542521","properties":{"name":"普兰县","cp":[81.176237,30.294402],"childNum":1},"geometry":{"type":"Polygon","coordinates":["@@]Ba@_FQFIHIJILONKNMJAHJTTn@JGTa@G@B\\ARAjERMHMBGNITSPAHITCDCBADALNJITSPHheXEBUHKFQFWBeCYCU@EBAHDHDFCHSBGREPIFSASCI@G@GDGFKJOHaBQAOHUHUTSRMTIPIHWRSN_hYXULKBQCMBKDIP@@UTUPYLgV[F[HK@CF@D@D@FBJBF@NCDADADCBCFAD@DAFAD@BCBABC@ABA@ADAB@FABADEHABCBEBABCDABABADABA@CBEDABABADBDAF@FAB@B@H@B@D@BCP@BAB@D@FALAFCZADADADBBBB@@BBDDBB@D@D@BAFBD@F@DBDBBDBBD@DBBBBDDBDBHBFBBBDBDBB@B@BBDFFDDBBBDBDBBBD@F@@@DBD@D@BAD@BADAB@F@BF@ĸO@@ABE@C@@@CDABABA@CBE@GDGBCBBBBBBD@B@DAB@DBL@FBB@DDDDHDFBHD@F@PCLCH@F@FJFBBD@B@F@BDDBDBBB@DAB@BCBC@ABADAD@B@@BBB@BBBB@D@B@B@BAB@FAFAB@D@B@D@BBBB@DBBB@B@HCB@BB@@ADCDBBBBBADADABCD@B@BBB@BBB@B@D@B@BBBB@DDDJBJ@HBDBJDLBFAHAJ@DBDDTDHBBDBBBBNJDDFDFFB@BBJBB@DDBDBDBDLPDFBBBBHDHDFBD@DDBB@BDPBD@F@D@BBBD@DDHHRPJPJN@BBFBFCLAN@@DJDDFBBDABCDEBCBCDCBA@C@E@CBKB@JEDAJABAD@DABADBBBD@B@BADCB@B@BBBB@@B@@EHAD@BBBDBBBD@FADAD@BBBBB@FBBBB@BDDBDBB@B@D@BALFTJJFNHHBPDNBPAbCH@B@BBBDBB@BBH@BBBFZAD@FBBVtBHDJNTBJ@FBBFF@D@DGFAHLDDBFBBDBDBDDDFFBBBDBJBDBDDDHFDBDBDDBBFFBJBHHL@BDDDFDFFDFDJFHFHDDBLDRJPJLLHDHRFDFB@HBLDDJBHADB@@@FAHADADBDBBDBB@BBBB@B@BA@@BCD@BDABAJAF@D@JAD@D@HFBD@BBBAD@@DDFRVHRANMHSFKLGPIEMCKAGPAVCRERJHRNLHJCRAFPDLDTORENNHP^FLDVBRJH@JCLALHPHBDLDNAHOFQHCTMJILOFKEIOCKADEFKNMPMHONERIR@VFNA\\QTETINGJL\\RJJH@XBRRJJBHL@JGNG@OBKAK@K@Q@GLIR@HPPBJCJQGQCGFCLGJCPKJKDGJKHILGRCRFJDDHAJADAP@JJFFJJFJFTHTDNCLGFGPOJKHODMAMBMDMFIJIPNZNTLdBNBFKFWBS@OHINMTITCN@V@RABGAGMMAGFCHIHK@MAKDKFMDIDITDVFR@V@LENOHOTMLEPBLCRJRHPCRKLBLFPAPAJCH@N@JCBGGOKOKICGDGHGJGBOBGGGFO@GDEFCLARBJEPCPEPCLDJNJJJHXJVFJDTAHDLDL@LKHIHGNEPELQDI@GEGEOHGLEXHL@DGHQZOJEHKJKHO@KAGBKLEZCTAXCNBFFFfDFDCD@D@B@B@DBDB@BB@BB@AB@BI@@DAD@DAH@DAFABAB@B@BBBFB@DBDBBB@DBD@DDB@DB@D@DAJDH@JADEDAFCJAH@HFHFBD@HANDFFDNLJNBDB@B@B@B@DBBBB@D@D@HAB@BA@ABA@@@I@ECA@ALEPADC@A@EBG@WA@CGACACAEAI@CBC@CBCBCBADABCNAHCFALED@FAD@BABABCBA@CAAAAECAA@C@EBI@CBADABCB@FABAPIBA@A@ABGBEBEBABABAB@B@B@DAFCBAFCHEBADADCDEDADC@@BCBEBCBC@A@C@CAA@E@CBEBCAE@C@ACC@AACACBBB@D@B@F@RCF@LBHBHBFBFB\\@H@J@D@H@DARABAFAJK^QECEAGEECEK@CDCBC@I@GACEE@@@@@AEACECCCECIAAIKCC@ABEBEDCBCBE@@@CDCBEBABEBEBABCBEBADEBCBABC@A@@@EAAB@@A@A@@@AAE@E@AFEBCBCBCDEBAFCFCBCBCBCDGDGDCFIBCDCDCFIFEAECGAE@I@IA@A@CAM@CBC@C@GECCAAE@C@@@@ABG@CB@BADABCHEBGC@IA@@AAA@AA@C@C@ABA@CB@AC@AA@@@GAE@CAC@C@EBEBEAECACACACA@AAA@EB@@A@A@C@A@CAAAA@A@IBA@@@A@@@A@AB@BCBC@A@CDABADAHAFADABA@CBA@CBA@EDABABAFABAD@@CB@BE@EBC@@BCBADCFCBCDCBEBEBGBE@KBKDEBEBABEBA@C@CBGBC@A@A@AAEACACBA@@@@B@DBH@D@BA@ABE@AB@@CBADABABEBABA@@@CA@C@E@AFABADEAE@CBC@Q@C@CHA@A@ACCCKCCGE@@EAGKA@C@C@CDEBEBCDEFKDG@A@@ECEAACOAE@CDG@E@AAA@@A@@B@D@BEBMDA@@D@J@FADCFABA@AB@HBBDDDBBFBBABCBCD@BBBDT@DBBA@A@C@A@ICC@MICAC@C@CAE@C@W@ABA@C@C@A@CBC@CB@J@BABABAFCDEHADCBABC@EBG@E@E@A@AB@D@BADADABEBC@@@@ABC@AAA@@ACkyA@AAC@A@C@CBCBCBA@C@ABCBA@A@A@A@A@C@@ABA@C@CFEAABABCB@BAACAC@CBADC@@@ABAHC@@@AAE@ACACEAA@CAC@AAEAACAA@C@AAACAA@EBE@ABEDK@ACEAGAAAAA@AA@C@C@E@ABA@@FCBABA@A@ACAEC@CCCACACECAAAAACAAAAACAAAAAEACACCAA@CCCACCGGCAGCE@GAACAACIEAEGKGMEIIQKOMQKEKOMEEKSA@@AC@A@EBC@ABCHARALGFS@SJGFENBLPPFLAZ@TFTJRLNKNK\\KVSVYFQHGAIIOQMKAAC@C@EDMHA@CBAAC@CCGAA@ADKHGAEGKQSIKAMDodCRMNI@[WIBmPUDWDQTKHEDOBS@UAMBcPODQBYAUBS@UBQFMFIHCHENEDO@YL_PYFuT[LWNKCCEJ]AEAIKGMEKFKFMHSHQHQAEGAIDYIKAKAEBQBSGIUBcDcN_DWP[V]ZSDIBQDQFG@MKIUFMLKTKPKEIIIW@M@CECKBKBIHQ@IQY@GLCdIJE@IIESMMGCCBERIJI@MKOOOIO@@GK@UDgAGGMUMUKKGSIQUOMCCCC@C@GAA@@E@C@AAA@A@CBA@@@A@AAAAA@@@A@ABABABC@AB@BA@AB@@@@@B@B@B@B@@ABABAB@@@@A@A@@@A@@@BEACU@AAsAKGAEBIf[NMFODU@OG]GSESIOIMKIGEICSAAEFGLGFKEMMCQE]CMHIFIJKBIEUK"],"encodeOffsets":[[83137,30730]]}}],"UTF8Encoding":true});}));