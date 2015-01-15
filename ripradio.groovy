#!/usr/bin/env groovy

// groovy version of the same script just for lolz
if (args.length < 1) {
    println "usage: ${System.properties['script.name']} <streamname> \n where <streamname> is dronezone, dubstep, groovesalad etc."
    System.exit(1)
} else {
    "streamripper http://ice.somafm.com/${args[0]} -d ${System.getenv().RIP_RADIO_HOME ?: "."} -u 'VLC/2.1.5 LibVLC/2.1.5' -q -r"
        .execute().consumeProcessOutput(System.out, System.err)
}
