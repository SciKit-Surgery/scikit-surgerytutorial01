//cs system, 
//z along barrel of scope,
//x horizontal
//y vertical

width=50;
linewidth=8;
rotate(-90,[0,0,1])
rotate(90,[0,1,0])
union()
{
translate([0,0,-(width/2)])
sphere(d=linewidth,$fn=30);
translate([0,0,(width/2)])
sphere(d=linewidth,$fn=30);
translate([0,0,-(width/2)])
cylinder(d=linewidth,h=width,$fn=30);

translate([0,-(width/2),0])
sphere(d=linewidth,$fn=30);
translate([0,(width/2),0])
sphere(d=linewidth,$fn=30);
rotate(90,[1,0,0])
translate([0,0,-(width/2)])
cylinder(d=linewidth,h=width,$fn=30);


translate([0,(-width/5),(-width/5)])
rotate(-45,[1,0,0])
cylinder(d=linewidth,h=width/1.4,$fn=30);
translate([0,(-width/5),(-width/5)])
sphere(d=linewidth,$fn=30);
translate([0,(width/3.27),(width/3.27)])
sphere(d=linewidth,$fn=30);

translate([0,(width/4),(-width/4)])
rotate(45,[1,0,0])
cylinder(d=linewidth,h=width/1.4,$fn=30);
translate([0,(width/4),(-width/4)])
sphere(d=linewidth,$fn=30);
translate([0,(-width/4),(width/4)])
sphere(d=linewidth,$fn=30);



}



