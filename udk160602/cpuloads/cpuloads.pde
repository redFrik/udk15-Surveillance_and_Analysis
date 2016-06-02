//use this together with cpuloads.py
import oscP5.*;
import netP5.*;
OscP5 oscP5;

FloatList loads= new FloatList();
int numCpu= 0;

void setup() {
  size(640, 480);
  OscProperties properties= new OscProperties();
  properties.setListeningPort(23456);  //osc receive port (from python)
  oscP5= new OscP5(this, properties);
}
void oscEvent(OscMessage msg) {
  if (msg.checkAddrPattern("/cpu")) {
    for (int i= 0; i<msg.arguments().length; i++) {
      loads.set(i, msg.get(i).floatValue());
    }
    numCpu= loads.size();
    //println(loads);  //debug
  }
}
void draw() {
  background(0);
  stroke(255);
  float spread= width/float(numCpu);
  for (int i= 0; i<numCpu; i++) {
    fill(map(loads.get(i), 0, 100, 0, 255));
    float x= i*spread+(spread*0.25);
    rect(x, 10, 50, height-20);
    fill(255);
    text("core "+(i+1)+"\n"+loads.get(i), x+5, 40);
  }
}