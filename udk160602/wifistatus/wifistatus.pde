//use this together with wifistatus_osx.py or wifistatus_linux.py
//green is wifi signal strength (rssi)
//white is wifi noise
import oscP5.*;
import netP5.*;
OscP5 oscP5;
int wstrength= -99;
int wnoise= -99;
void setup() {
  size(640, 480);
  OscProperties properties= new OscProperties();
  properties.setListeningPort(12345);  //osc receive port (from python)
  oscP5= new OscP5(this, properties);
  background(0);
}
void oscEvent(OscMessage msg) {
  if (msg.checkAddrPattern("/wifi")) {
    wstrength= msg.get(0).intValue();
    wnoise= msg.get(1).intValue();
  }
}
void draw() {
  noStroke();
  fill(0, 5);  //trail
  rect(0, 0, width, height);
  
  int x= frameCount%width;
  stroke(0);
  line(x, 0, x, height);    //erase row
  stroke(0, 255, 0);  //green
  line(x, map(wstrength, -99, 0, height, 0), x, height);
  stroke(255, 255, 255);  //white
  point(x, map(wnoise, -99, 0, height, 0));
  
  fill(0);
  rect(0, 0, 100, 30);
  fill(255);
  text("strength: "+wstrength, 8, 12);
  text("noise: "+wnoise, 8, 24);
}