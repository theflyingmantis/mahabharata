#include<iostream>
#include<math.h>
#include<fstream>
#include<string>
using namespace std;
int main()
{
   string line1,line2,garbage;
ifstream myfile ("board_file.txt");
if (myfile.is_open())
{
	myfile>>garbage;
    while ( myfile.good() )
    {
        myfile>>line1>>line2;
        if(line2=="U")
        {cout << line1;break;}
    }
    myfile.close();
}
}
