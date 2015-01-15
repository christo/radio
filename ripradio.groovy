#!/usr/bin/env groovy

if (args.length < 1) {
    println "usage: ripsoma.groovy <streamname> \n where <streamname> is dronezone, dubstep, groovesalad etc."
    System.exit(1)
} else {
    def dir = System.getenv().RIP_RADIO_HOME ?: "."
    def p = "streamripper http://ice.somafm.com/${args[0]} -d $dir -u 'VLC/2.1.5 LibVLC/2.1.5' -q -r"
    println p
    
    //def p = "streamripper http://ice.somafm.com/${args[0]} -d $dir -u 'VLC/2.1.5 LibVLC/2.1.5' -q -r".execute()
    //p.consumeProcessOutput(System.out, System.err)
}
