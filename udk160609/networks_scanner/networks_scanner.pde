//use together with networks_scanner_osx.py or networks_scanner_linux.py
final int MAXNUM= 100; 

import oscP5.*;
import netP5.*;
OscP5 oscP5;

String data[]= new String[MAXNUM];  //max 100 networks

void setup() {
  size(800, 600);
  OscProperties properties= new OscProperties();
  properties.setListeningPort(34567);  //osc receive port (from python)
  oscP5= new OscP5(this, properties);
  noSmooth();
}
void oscEvent(OscMessage msg) {
  if (msg.checkAddrPattern("/num_networks")) {
    int num= msg.get(0).intValue();
    if (num>MAXNUM) {
      println("warning: max "+MAXNUM+" networks");
    }
    for (int i= 0; i<MAXNUM; i++) {
      data[i]= "";  //clear strings
    }
  } else if (msg.checkAddrPattern("/networks")) {
    int index= msg.get(0).intValue();
    String network= msg.get(1).stringValue();
    if (index<MAXNUM) {
      data[index]= network;
    }
  }
}
void draw() {
  background(0);
  fill(255);
  for (int i= 0; i<MAXNUM; i++) {
    if (data[i]!=null) {
      text(data[i], 10, i*12+12);
    }
  }
}