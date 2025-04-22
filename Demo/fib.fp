#This is a FooProg demo
#Reads n,then calculates the first n numbers in the fibonacci sequence
#(starts with 0)
$a$=0;
$b$=1;
read $c$;
do{
	write $a$;
	$d$=$a$+$b$;
	$a$=$b$;
	$b$=$d$;
	$c$=$c$-1;
}while $c$;



