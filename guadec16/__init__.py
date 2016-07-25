#!/usr/bin/python

import subprocess
import os.path
from renderlib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'https://events.opensuse.org/conference/oSC16/schedule.xml'

# For (really) too long titles
titlemap = {
    #
}

def bounce(i, min, max, frames):
    if i == frames - 1:
        return 0

    if i <= frames/2:
        return easeInOutQuad(i, min, max, frames/2)
    else:
        return max - easeInOutQuad(i - frames/2, min, max, frames/2)

def introFrames(parameters):
    firstmove=2100
    move=100

    # 2 Sekunden stehen lassen
    frames = fps
    for i in range(0, frames):
        yield (
            ('title', 'style',    'opacity', "0"),
            ('presentedby', 'style',    'opacity', "0"),
            ('speaker', 'style',    'opacity', "0"),
            ('overlay', 'style',    'opacity', "0"),
            ('guadeclogo', 'style',    'opacity', "0"),
            ('onhold', 'style',    'opacity', "0"),
            ('onlinediscussion', 'style',    'opacity', "0"),
        )

    # 0.25 text fade in
    frames = int(fps/2)
    for i in range(0, frames):
        yield (
            ('guadeclogo', 'style',    'opacity', "%.4f" % easeLinear(i, 0, 1, frames-1)),
            ('overlay', 'style',    'opacity', "%.4f" % easeLinear(i, 0, 1, frames-1)),
            ('overlay', 'attr',     'transform', 'translate(0, %.4f)' % easeOutQuad(i, firstmove, -firstmove, frames-1)),
        )

    # 2 Sekunden stehen lassen
    frames = int(fps/1.5)
    for i in range(0, frames):
        yield ()

    # 0.25 text fade in
    frames = int(fps/5)
    for i in range(0, frames):
        yield (
            ('title', 'style',    'opacity', "%.4f" % easeLinear(i, 0, 1, frames-1)),
            ('titletranslator', 'attr',     'transform', 'translate(0, %.4f)' % easeOutQuad(i, -move, move, frames-1)),
        )

    # 0.25 text fade in
    frames = int(fps/5)
    for i in range(0, frames):
        yield (
            ('presentedby', 'style',    'opacity', "%.4f" % easeLinear(i, 0, 1, frames-1)),
            ('presentedby', 'attr',     'transform', 'translate(0, %.4f)' % easeOutQuad(i, -move, move, frames-1)),
        )
    # 0.25 text fade in
    frames = int(fps/5)
    for i in range(0, frames):
        yield (
            ('speaker', 'style',    'opacity', "%.4f" % easeLinear(i, 0, 1, frames-1)),
            ('speakertranslator', 'attr',     'transform', 'translate(0, %.4f)' % easeOutQuad(i, -move, move, frames-1)),
            ('onhold', 'style',    'opacity', "%.4f" % easeLinear(i, 0, 1, frames-1)),
            ('onhold', 'attr',     'transform', 'translate(0, %.4f)' % easeOutQuad(i, -move, move, frames-1)),
            ('onlinediscussion', 'style',    'opacity', "%.4f" % easeLinear(i, 0, 1, frames-1)),
        )

    # 2 Sekunden stehen lassen
    frames = 3*fps
    for i in range(0, frames):
        yield (
            ('title', 'style',    'opacity', "1"),
            ('presentedby', 'style',    'opacity', "1"),
            ('onhold', 'style',    'opacity', "1"),
            ('speaker', 'style',    'opacity', "1"),
        )

def outroFrames(p):
    # 2 Sekunden stehen lassen
    frames = int(fps/20)
    for i in range(0, frames):
        yield (
            ('title', 'style',    'opacity', "0"),
        )

    # 5 Sekunden stehen bleiben
    frames = 5*fps
    for i in range(0, frames):
#matrix(1.1478962,0,0,1.1478962,-974.48807,-78.402379)
#matrix(1.5838009,0,0,1.5838009,-3846.6634,-309.48307)
#matrix(1.638289,0,0,1.638289,-4205.6854,-338.36816)
        scale =easeLinear(i, 1.0, 1.638289, frames-1)
        #b1 =easeLinear(i,     0.0, 0.0, frames-1)
        #c1 =easeLinear(i,     0.0, 0.0, frames-1)
        #d1 =easeLinear(i,     1.0, 1.638289, frames-1)
        #e1 =easeLinear(i, 0.0, -4205.6854, frames-1)
        #f1 =easeLinear(i, 0.0, -338.36816, frames-1)
        yield (
            ('guadeclogoscale', 'attr', 'transform', 'scale({scale},{scale})'.format(scale=scale),),
            #('group-transform', 'attr',     'translate', 'translate(-560.16939,1.7212031)',),
            #('guadeclogo', 'attr',    'opacity', "%.4f" % easeLinear(i, 0, 1, frames-1)),
            #('guadeclogo', 'attr',     'transform', 'matrix({a}, {b}, {c}, {d}, {e}, {f})'.format(a=a1, b=b1, c=c1, d=d1, e=e1, f=f1,)) ,
            #('guadec-logo, 'attr',     'transform', 'matrix({scalefac}, 0, 0, {scalefac}, {calcx}, {calcy})'.format(scalefac=scalenumber,calcx=scalenumber*560.16939,calcy=scalenumber*-1.7212031)) ,
            #   ('group-transform', 'attr',     'translate', 'translate(560.16939,-1.7212031)',),
        )

def debug():
#    render(
#      'intro.svg',
#      '../intro.ts',
#      introFrames,
#      {
#          '$ID': 4711,
#          '$title': "Long Long Long title is LONG",
#          '$sub': 'Long Long Long Long subtitle is LONGER',
#          '$speaker': 'Long Name of Dr. Dr. Prof. Dr. Long Long'
#      }
#    )

#    render(
#        'pause.svg',
#        '../pause.ts',
#        introFrames,
#        {
#          '$title': "Long Long Long title is LONG",
#        }
#    )

    render(
      'outro.svg',
      '../outro.ts',
      outroFrames
    )

def tasks(queue, args):
    # iterate over all events extracted from the schedule xml-export
    for event in events(scheduleUrl):

        if len(args) > 0:
            if not str(event['id']) in args:
                continue

        # generate a task description and put it into the queue
        queue.put(Rendertask(
            infile = 'intro.svg',
            outfile = str(event['id'])+".ts",
            sequence = introFrames,
            parameters = {
                '$ID': event['id'],
                '$TITLE': event['title'],
                '$SUBTITLE': event['subtitle'],
                '$SPEAKER': event['personnames']
                }
            ))
