#!/usr/bin/env python3
"""Write a Kdenlive project for the `preview-render` operation (9.5 follow-ups
spec, decisions 7–10): one video track carrying the (video-only) clip
with an unsharp filter, one empty audio track, the timeline zone set to the
whole clip, so that
Add Preview Zone + Start Preview Render renders every 25-frame chunk.

kdenlive_project.py <clip> <frames> <fps> <out.kdenlive> [--kdenlive-version V] [--mlt-version V]

Shape after Kdenlive's sequence-based document format (23.04+; main_bin
playlist carrying kdenlive:docproperties.*, one sequence tractor with
kdenlive:sequenceproperties.*, a final_tractor), as written by Kdenlive
and as in a third-party generated example; frame times as timecodes.
The unsharp filter is MLT's avfilter.unsharp with PCMark 10's Video Editing
sharpening parameters (Technical Guide p. 76: unsharp lx=7:ly=7:la=0.56:
cx=7:cy=7:ca=0.28).
"""

import argparse
import uuid


def tc(frames, fps):
    s = frames / fps
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{sec:06.3f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clip"); ap.add_argument("frames", type=int); ap.add_argument("fps", type=int); ap.add_argument("out")
    ap.add_argument("--kdenlive-version", default="23.08.5"); ap.add_argument("--mlt-version", default="7.22.0")
    a = ap.parse_args()
    seq = "{" + str(uuid.uuid4()) + "}"
    last = a.frames - 1
    out = tc(last, a.fps)
    xml = f"""<?xml version='1.0' encoding='utf-8'?>
<mlt LC_NUMERIC="C" producer="main_bin" version="{a.mlt_version}">
  <profile colorspace="709" description="HD 1080p {a.fps} fps" display_aspect_den="9" display_aspect_num="16" frame_rate_den="1" frame_rate_num="{a.fps}" height="1080" progressive="1" sample_aspect_den="1" sample_aspect_num="1" width="1920"/>
  <producer id="black_track" in="00:00:00.000" out="{out}">
    <property name="length">2147483647</property>
    <property name="eof">continue</property>
    <property name="resource">black</property>
    <property name="aspect_ratio">1</property>
    <property name="mlt_service">color</property>
    <property name="kdenlive:playlistid">black_track</property>
    <property name="mlt_image_format">rgba</property>
    <property name="set.test_audio">0</property>
  </producer>
  <chain id="chain0" out="{out}">
    <property name="length">{a.frames}</property>
    <property name="eof">pause</property>
    <property name="resource">{a.clip}</property>
    <property name="mlt_service">avformat-novalidate</property>
    <property name="kdenlive:clipname">clip</property>
    <property name="kdenlive:id">3</property>
    <property name="kdenlive:clip_type">0</property>
    <property name="kdenlive:folderid">-1</property>
  </chain>
  <playlist id="playlist0"/>
  <playlist id="playlist1"/>
  <tractor id="tractor0" in="00:00:00.000" out="{out}">
    <property name="kdenlive:audio_track">1</property>
    <track hide="video" producer="playlist0"/>
    <track hide="video" producer="playlist1"/>
  </tractor>
  <playlist id="playlist2">
    <entry in="00:00:00.000" out="{out}" producer="chain0">
      <filter id="filter1">
        <property name="mlt_service">avfilter.unsharp</property>
        <property name="kdenlive_id">avfilter.unsharp</property>
        <property name="av.luma_msize_x">7</property>
        <property name="av.luma_msize_y">7</property>
        <property name="av.luma_amount">0.56</property>
        <property name="av.chroma_msize_x">7</property>
        <property name="av.chroma_msize_y">7</property>
        <property name="av.chroma_amount">0.28</property>
      </filter>
    </entry>
  </playlist>
  <playlist id="playlist3"/>
  <tractor id="tractor1" in="00:00:00.000" out="{out}">
    <track hide="audio" producer="playlist2"/>
    <track hide="audio" producer="playlist3"/>
  </tractor>
  <tractor id="{seq}" in="00:00:00.000" out="{out}">
    <property name="kdenlive:uuid">{seq}</property>
    <property name="kdenlive:clipname">Sequence 1</property>
    <property name="kdenlive:sequenceproperties.hasAudio">1</property>
    <property name="kdenlive:sequenceproperties.hasVideo">1</property>
    <property name="kdenlive:sequenceproperties.activeTrack">1</property>
    <property name="kdenlive:sequenceproperties.tracksCount">2</property>
    <property name="kdenlive:sequenceproperties.documentuuid">{seq}</property>
    <property name="kdenlive:duration">{out}</property>
    <property name="kdenlive:maxduration">{a.frames}</property>
    <property name="kdenlive:producer_type">17</property>
    <property name="kdenlive:id">2</property>
    <property name="kdenlive:clip_type">0</property>
    <property name="kdenlive:folderid">-1</property>
    <property name="kdenlive:sequenceproperties.audioTarget">0</property>
    <property name="kdenlive:sequenceproperties.videoTarget">1</property>
    <property name="kdenlive:sequenceproperties.disablepreview">0</property>
    <property name="kdenlive:sequenceproperties.position">0</property>
    <property name="kdenlive:sequenceproperties.scrollPos">0</property>
    <property name="kdenlive:sequenceproperties.tracks">2</property>
    <property name="kdenlive:sequenceproperties.verticalzoom">1</property>
    <property name="kdenlive:sequenceproperties.zonein">0</property>
    <property name="kdenlive:sequenceproperties.zoneout">{last}</property>
    <property name="kdenlive:sequenceproperties.zoom">8</property>
    <track producer="black_track"/>
    <track producer="tractor0"/>
    <track producer="tractor1"/>
    <transition id="transition0">
      <property name="a_track">0</property>
      <property name="b_track">1</property>
      <property name="mlt_service">mix</property>
      <property name="kdenlive_id">mix</property>
      <property name="internal_added">237</property>
      <property name="always_active">1</property>
      <property name="accepts_blanks">1</property>
      <property name="sum">1</property>
    </transition>
    <transition id="transition1">
      <property name="a_track">0</property>
      <property name="b_track">2</property>
      <property name="mlt_service">frei0r.cairoblend</property>
      <property name="kdenlive_id">frei0r.cairoblend</property>
      <property name="internal_added">237</property>
      <property name="always_active">1</property>
      <property name="disable">0</property>
    </transition>
  </tractor>
  <playlist id="main_bin">
    <property name="kdenlive:docproperties.audioChannels">2</property>
    <property name="kdenlive:docproperties.documentid">1758000000000</property>
    <property name="kdenlive:docproperties.enableTimelineZone">1</property>
    <property name="kdenlive:docproperties.enableproxy">0</property>
    <property name="kdenlive:docproperties.generateimageproxy">0</property>
    <property name="kdenlive:docproperties.generateproxy">0</property>
    <property name="kdenlive:docproperties.kdenliveversion">{a.kdenlive_version}</property>
    <property name="kdenlive:docproperties.previewextension"/>
    <property name="kdenlive:docproperties.previewparameters"/>
    <property name="kdenlive:docproperties.proxyextension"/>
    <property name="kdenlive:docproperties.proxyparams"/>
    <property name="kdenlive:docproperties.uuid">{seq}</property>
    <property name="kdenlive:docproperties.version">1.1</property>
    <property name="kdenlive:docproperties.opensequences">{seq}</property>
    <property name="kdenlive:docproperties.activetimeline">{seq}</property>
    <property name="kdenlive:expandedFolders"/>
    <property name="kdenlive:binZoom">4</property>
    <property name="kdenlive:documentnotes"/>
    <property name="xml_retain">1</property>
    <entry in="00:00:00.000" out="{out}" producer="{seq}"/>
    <entry in="00:00:00.000" out="{out}" producer="chain0"/>
  </playlist>
  <tractor id="final_tractor" in="00:00:00.000" out="{out}">
    <property name="kdenlive:projectTractor">1</property>
    <track in="00:00:00.000" out="{out}" producer="{seq}"/>
  </tractor>
</mlt>
"""
    open(a.out, "w").write(xml)


if __name__ == "__main__":
    main()
