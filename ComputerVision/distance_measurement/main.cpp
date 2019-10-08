#include <iostream>
#include "common.h"
using namespace std;



int main(int argc, const char * argv[])
{
	int flag = 0;
	if (flag == 0)
	{ 
		cout << "This will find vanish-point offset....." << endl;
		main_setVanPoffset(argc, argv);
	}
	else if (flag == 1)
	{
		cout << "measure will begin....." << endl;
		main_measure(argc, argv);
	}
	else if (flag == 2)
	{
		image_save();
	}
		

	cout << "It's ok!" << endl;
	while (1);
	return 0;
}