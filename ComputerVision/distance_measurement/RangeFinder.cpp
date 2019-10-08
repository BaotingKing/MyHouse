#include <string>
#include <fstream>
#include "RangeFinder.hpp"
#include <tuple>
#include <vector>


using namespace std;
#include <iostream>

//btm is 920 when testing
void RangeFinder::initialize() {
    ifstream input("vanishingPoffset.txt");
	if(input.is_open()){
		string number;
		getline(input,number);           //read number
		//istream::getline(input, number);
		vanishingPoffset = atoi(number.c_str()); //convert to integer
		//  cout<<vanishingPoffset<<endl; //print it out
    }

    /*
	if(Angle == 0)
	a=0;
	else if(Angle==10)
	a=150;                 155
	else if(Angle==20)
	a=340;                 345
	*/
	
	if (false)
	{
		RangeTable140.push_back(make_tuple((360 - 380), 300));
		RangeTable140.push_back(make_tuple((360 - 265), 500));
		RangeTable140.push_back(make_tuple((360 - 173), 800));
		RangeTable140.push_back(make_tuple((360 - 133), 1000));
		RangeTable140.push_back(make_tuple((360 - 100), 1200));
		RangeTable140.push_back(make_tuple((360 - 80), 1600));
		RangeTable140.push_back(make_tuple((360 - 65), 2000));
		RangeTable140.push_back(make_tuple((360 - 50), 2500));
		RangeTable140.push_back(make_tuple((360 - 41), 3000));

		RangeTable140.push_back(make_tuple((360 - 29), 4000));
		RangeTable140.push_back(make_tuple((360 - 22), 5000));
		RangeTable140.push_back(make_tuple((360 - 18), 6000));
		RangeTable140.push_back(make_tuple((360 - 15), 7000));
		RangeTable140.push_back(make_tuple((360 - 13), 8000));
		RangeTable140.push_back(make_tuple((360 - 12), 9000));


		RangeTable150.push_back(make_tuple((360 - 440), 300));
		RangeTable150.push_back(make_tuple((360 - 283), 500));
		RangeTable150.push_back(make_tuple((360 - 187), 800));
		RangeTable150.push_back(make_tuple((360 - 141), 1000));
		RangeTable150.push_back(make_tuple((360 - 105), 1200));
		RangeTable150.push_back(make_tuple((360 - 83), 1600));
		RangeTable150.push_back(make_tuple((360 - 67), 2000));
		RangeTable150.push_back(make_tuple((360 - 52), 2500));
		RangeTable150.push_back(make_tuple((360 - 43), 3000));

		RangeTable150.push_back(make_tuple((360 - 30), 4000));
		RangeTable150.push_back(make_tuple((360 - 22), 5000));
		RangeTable150.push_back(make_tuple((360 - 18), 6000));
		RangeTable150.push_back(make_tuple((360 - 15), 7000));
		RangeTable150.push_back(make_tuple((360 - 13), 8000));
		RangeTable150.push_back(make_tuple((360 - 12), 9000));
		
		RangeTable160.push_back(make_tuple((360 - 500), 300));   //85 500
		RangeTable160.push_back(make_tuple((360 - 300), 500));     //247 300
		RangeTable160.push_back(make_tuple((360 - 200), 800));  //340 200
		RangeTable160.push_back(make_tuple((360 - 149), 1000));
		RangeTable160.push_back(make_tuple((360 - 110), 1200));    //390 127
		RangeTable160.push_back(make_tuple((360 - 86), 1600));//420
		RangeTable160.push_back(make_tuple((360 - 70), 2000));
		RangeTable160.push_back(make_tuple((360 - 55), 2500));
		RangeTable160.push_back(make_tuple((360 - 45), 3000)); //445
		RangeTable160.push_back(make_tuple((360 - 52), 3300));////458
		RangeTable160.push_back(make_tuple((360 - 31), 4000));
		RangeTable160.push_back(make_tuple((360 - 41), 4500));  //4
		RangeTable160.push_back(make_tuple((360 - 23), 5000));
		RangeTable160.push_back(make_tuple((360 - 18), 6000));
		RangeTable160.push_back(make_tuple((360 - 15), 7000));
		RangeTable160.push_back(make_tuple((360 - 13), 8000));
		RangeTable160.push_back(make_tuple((360 - 12), 9000));

		RangeTable170.push_back(make_tuple((360 - 560), 300));
		RangeTable170.push_back(make_tuple((360 - 317), 500));
		RangeTable170.push_back(make_tuple((360 - 212), 800));
		RangeTable170.push_back(make_tuple((360 - 158), 1000));
		RangeTable170.push_back(make_tuple((360 - 115), 1200));
		RangeTable170.push_back(make_tuple((360 - 89), 1600));
		RangeTable170.push_back(make_tuple((360 - 73), 2000));
		RangeTable170.push_back(make_tuple((360 - 57), 2500));
		RangeTable170.push_back(make_tuple((360 - 47), 3000));
		RangeTable170.push_back(make_tuple((360 - 56), 3300));
		RangeTable170.push_back(make_tuple((360 - 32), 4000));
		RangeTable170.push_back(make_tuple((360 - 44), 4500));
		RangeTable170.push_back(make_tuple((360 - 23), 5000));
		RangeTable170.push_back(make_tuple((360 - 18), 6000));
		RangeTable170.push_back(make_tuple((360 - 15), 7000));
		RangeTable170.push_back(make_tuple((360 - 13), 8000));
		RangeTable170.push_back(make_tuple((360 - 12), 9000));
		
		/*
		RangeTable200.push_back(make_tuple((-205) , 3000));
		RangeTable200.push_back(make_tuple((-20) , 500));
		RangeTable200.push_back(make_tuple((110) , 800));
		RangeTable200.push_back(make_tuple((190) , 1200));
		RangeTable200.push_back(make_tuple((245) , 1600));
		RangeTable200.push_back(make_tuple((278) , 2400));
		RangeTable200.push_back(make_tuple((301) , 3300));
		RangeTable200.push_back(make_tuple((315) , 4500));
		RangeTable200.push_back(make_tuple((325) , 6000));
		RangeTable200.push_back(make_tuple((329) , 7200));
		RangeTable200.push_back(make_tuple((334) , 9500));
		RangeTable200.push_back(make_tuple((339) , 12200));
		RangeTable200.push_back(make_tuple((341) , 15000));
		RangeTable200.push_back(make_tuple((343) , 20000));
		*/
	}
	else
	{
		int offset = -11;
		RangeTable150.push_back(make_tuple((480 - 495 + offset), 300));     //The distance from the target to the bottom of the pixel
		RangeTable150.push_back(make_tuple((480 - 465 + offset), 350));
		RangeTable150.push_back(make_tuple((480 - 444 + offset), 400));
		RangeTable150.push_back(make_tuple((480 - 427 + offset), 450));
		RangeTable150.push_back(make_tuple((480 - 412 + offset), 500));
		RangeTable150.push_back(make_tuple((480 - 400 + offset), 550));

		RangeTable150.push_back(make_tuple((480 - 390 + offset), 600));
		RangeTable150.push_back(make_tuple((480 - 381 + offset), 650));
		RangeTable150.push_back(make_tuple((480 - 374 + offset), 700));
		RangeTable150.push_back(make_tuple((480 - 367 + offset), 750));
		RangeTable150.push_back(make_tuple((480 - 362 + offset), 800));
		RangeTable150.push_back(make_tuple((480 - 352 + offset), 900));
		RangeTable150.push_back(make_tuple((480 - 346 + offset), 1000));

		RangeTable160.push_back(make_tuple((480 - 458 + offset), 300));   //85 500
		RangeTable160.push_back(make_tuple((480 - 424 + offset), 350));
		RangeTable160.push_back(make_tuple((480 - 400 + offset), 400));
		RangeTable160.push_back(make_tuple((480 - 380 + offset), 450));
		RangeTable160.push_back(make_tuple((480 - 365 + offset), 500));
		RangeTable160.push_back(make_tuple((480 - 342 + offset), 600));
		RangeTable160.push_back(make_tuple((480 - 325 + offset), 700));
		RangeTable160.push_back(make_tuple((480 - 318 + offset), 750));
		RangeTable160.push_back(make_tuple((480 - 312 + offset), 800));
		RangeTable160.push_back(make_tuple((480 - 302 + offset), 900));
		RangeTable160.push_back(make_tuple((480 - 295 + offset), 1000));     //247 300
	

		RangeTable170.push_back(make_tuple((480 - 478 + offset), 300));
		RangeTable170.push_back(make_tuple((480 - 444 + offset), 350));
		RangeTable170.push_back(make_tuple((480 - 418 + offset), 400));
		RangeTable170.push_back(make_tuple((480 - 397 + offset), 450));
		RangeTable170.push_back(make_tuple((480 - 381 + offset), 500));
		RangeTable170.push_back(make_tuple((480 - 356 + offset), 600));
		RangeTable170.push_back(make_tuple((480 - 337 + offset), 700));
		RangeTable170.push_back(make_tuple((480 - 330 + offset), 750));
		RangeTable170.push_back(make_tuple((480 - 324 + offset), 800));
		RangeTable170.push_back(make_tuple((480 - 315 + offset), 900));
		RangeTable170.push_back(make_tuple((480 - 306 + offset), 1000));
	}   

}



int RangeFinder::getRange(int BoxBtm, int CameraHeight) {
    //RangeTable120.push_back(make_tuple(35 , 300));

    int AdjusteBtm = BoxBtm+vanishingPoffset;  //!!!! positive vp means the vline is lower and the adjustbtm should be treated as higher
    int CamLower = 0;
    int CamHigher = 0;
    int RangeCamLower = 0;
    int RangeCamHigher = 0;
    int Range = 0;
    int IndexNear;
    int IndexFar;

    if (CameraHeight > 170 || CameraHeight < 140)                             /////Camera height is limited to: 140CM-170CM
        return -1;


    if (CameraHeight >= 140 && CameraHeight<150)
    {
        CamLower = 140;
        CamHigher = 150;

    }
    else if (CameraHeight >= 150 && CameraHeight<160)
    {
        CamLower = 150;
        CamHigher = 160;

    }
    else if (CameraHeight >= 160 && CameraHeight<170)
    {
        CamLower = 160;
        CamHigher = 170;

    }
    /*
        else if (CameraHeight >= 180 && CameraHeight <= 200)
        {
                CamLower = 180;
                CamHigher = 200;

        }
*/
    ////////////////////////////////////////////
	if (CamLower == 140)
	{
		{
			int x = RangeTable140.size()-1;
            //cout << x;
            //cout <<" RangeTable120[x]="<<get<0>(RangeTable120[x])<<endl;

            if(AdjusteBtm>get<0>(RangeTable140[x]))
            {
                RangeCamLower =20000;
                goto endof140;
            }

            if(AdjusteBtm<get<0>(RangeTable140[0]))
            {
                RangeCamLower =get<1>(RangeTable140[0]);
                goto endof140;
            }
            //cout<<"AdjusteBtm="<<AdjusteBtm<<endl;
			
			if(AdjusteBtm>get<0>(RangeTable140[x/2]))
			{
				for (int i = x / 2; i <= x; i++)
				{
					if (get<0>(RangeTable140[i]) <= AdjusteBtm&&get<0>(RangeTable140[i + 1]) >= AdjusteBtm)
					{
						IndexNear = i;
						IndexFar = i + 1;
						break;
					}
				}
			}
			else
			{
				for (int i = 0; i <= x/2; i++)
				{
					if (get<0>(RangeTable140[i]) <= AdjusteBtm&&get<0>(RangeTable140[i + 1]) >= AdjusteBtm)
					{
						IndexNear = i;
						IndexFar = i + 1;
						break;
					}
				}
			}
			//cout << "near=" << IndexNear<<endl;
            ///cout << "far=" << IndexFar<<endl;
			RangeCamLower = get<1>(RangeTable140[IndexNear]) + (get<1>(RangeTable140[IndexFar]) - get<1>(RangeTable140[IndexNear]))  *  (AdjusteBtm - get<0>(RangeTable140[IndexNear])) / (get<0>(RangeTable140[IndexFar]) - get<0>(RangeTable140[IndexNear]));			
			//cout<<"RangeCamLower="<<RangeCamLower<<endl;
		}
	
	endof140:
		int a =1;
	}   //120


    if (CamLower == 150||CamHigher ==150)
	{
		{
			int x = RangeTable150.size() - 1;
			//cout << x;
			//cout <<" RangeTable120[0]="<<get<0>(RangeTable120[0]);
			if(AdjusteBtm>get<0>(RangeTable150[x]))
			{
				if(CamLower == 150)
					RangeCamLower =20000;
				else
					RangeCamHigher =20000;
				
				goto endof150;
			}
			
			if(AdjusteBtm<get<0>(RangeTable150[0]))
			{
				if(CamLower == 150)
					RangeCamLower =get<1>(RangeTable150[0]);
				else
					RangeCamHigher =get<1>(RangeTable150[0]);

                goto endof150;
            }

            if (AdjusteBtm>get<0>(RangeTable150[x / 2]))
			{
				for (int i = x / 2; i <= x; i++)
				{
					if (get<0>(RangeTable150[i]) <= AdjusteBtm && get<0>(RangeTable150[i + 1]) >= AdjusteBtm)
					{
						IndexNear = i;
						IndexFar = i + 1;
						break;
					}
				}
			}
			else
            {
				for (int i = 0; i <= x / 2; i++)
				{
					if (get<0>(RangeTable150[i]) <= AdjusteBtm && get<0>(RangeTable150[i + 1]) >= AdjusteBtm)
					{
						IndexNear = i;
						IndexFar = i + 1;
						break;
					}
				}
			}
			//cout << "near=" << IndexNear;
			//cout << "far=" << IndexFar<<endl;
			if(CamLower ==150)
				RangeCamLower = get<1>(RangeTable150[IndexNear]) + (get<1>(RangeTable150[IndexFar]) - get<1>(RangeTable150[IndexNear]))  *  (AdjusteBtm - get<0>(RangeTable150[IndexNear])) / (get<0>(RangeTable150[IndexFar]) - get<0>(RangeTable150[IndexNear]));
			else if(CamHigher ==150)
				RangeCamHigher= get<1>(RangeTable150[IndexNear]) + (get<1>(RangeTable150[IndexFar]) - get<1>(RangeTable150[IndexNear]))  *  (AdjusteBtm - get<0>(RangeTable150[IndexNear])) / (get<0>(RangeTable150[IndexFar]) - get<0>(RangeTable150[IndexNear]));
			
			// cout<<"RangeCamHigher="<<RangeCamHigher<<endl;
		}
	
	endof150:
		int a =1;
	} //140
	
	if (CamLower == 160 || CamHigher == 160)
	{
		{
			int x = RangeTable160.size() - 1;
			//cout << x;
            //cout <<" RangeTable120[0]="<<get<0>(RangeTable120[0]);
			if(AdjusteBtm>get<0>(RangeTable160[x]))
			{
				if(CamLower == 160)
					RangeCamLower =20000;
				else
					RangeCamHigher =20000;
				goto endof160;
			}
			
			if(AdjusteBtm<get<0>(RangeTable160[0]))
			{
				if(CamLower == 160)
					RangeCamLower =get<1>(RangeTable160[0]);
				else
					RangeCamHigher =get<1>(RangeTable160[0]);
				goto endof160;
			}
			
			if (AdjusteBtm>get<0>(RangeTable160[x / 2]))
			{
				for (int i = x / 2; i <= x; i++)
				{
					if (get<0>(RangeTable160[i]) <= AdjusteBtm && get<0>(RangeTable160[i + 1]) >= AdjusteBtm)
					{
						IndexNear = i;
						IndexFar = i + 1;
						break;
					}
				}
			}
			else
			{
                for (int i = 0; i <= x / 2; i++)
				{
					if (get<0>(RangeTable160[i]) <= AdjusteBtm && get<0>(RangeTable160[i + 1]) >= AdjusteBtm)
					{
						IndexNear = i;
						IndexFar = i + 1;
						break;
					}
				}
			}
			
			//cout << "near=" << IndexNear;
            //cout << "far=" << IndexFar<<endl;
			
			if (CamLower == 160)
				RangeCamLower = get<1>(RangeTable160[IndexNear]) + (get<1>(RangeTable160[IndexFar]) - get<1>(RangeTable160[IndexNear]))  *  (AdjusteBtm - get<0>(RangeTable160[IndexNear])) / (get<0>(RangeTable160[IndexFar]) - get<0>(RangeTable160[IndexNear]));
			else if (CamHigher == 160)
				RangeCamHigher = get<1>(RangeTable160[IndexNear]) + (get<1>(RangeTable160[IndexFar]) - get<1>(RangeTable160[IndexNear]))  *  (AdjusteBtm - get<0>(RangeTable160[IndexNear])) / (get<0>(RangeTable160[IndexFar]) - get<0>(RangeTable160[IndexNear]));
				
		}
		
	endof160:
		int a =1;
	} //160
	
	if (CamLower == 170 || CamHigher == 170)
	{
		{
			int x = RangeTable170.size() - 1;
			//cout << x;
            //cout <<" RangeTable120[0]="<<get<0>(RangeTable120[0]);
            // cout<<get<0>(RangeTable180[x])<<endl;
            if(AdjusteBtm>get<0>(RangeTable170[x]))
            {
                if(CamLower == 170)
                    RangeCamLower =20000;
                else
                    RangeCamHigher =20000;
                goto endof170;
            }

            if(AdjusteBtm<get<0>(RangeTable170[0]))
			{
				if(CamLower == 170)
					RangeCamLower =get<1>(RangeTable170[0]);
				else
					RangeCamHigher =get<1>(RangeTable170[0]);
				goto endof170;
			}

            if (AdjusteBtm>get<0>(RangeTable170[x / 2]))
			{
				//cout<<"ADM="<<AdjusteBtm<<endl;
                //cout<<"large"<<endl;
                for (int i = x / 2; i <= x; i++)
				{
					if (get<0>(RangeTable170[i]) <= AdjusteBtm && get<0>(RangeTable170[i + 1]) >= AdjusteBtm)
					{
						IndexNear = i;
						IndexFar = i + 1;
						break;
					}
				}
			}
			else
            {
				for (int i = 0; i <= x / 2; i++)
				{
					//cout<<"small"<<endl;
					if (get<0>(RangeTable170[i]) <= AdjusteBtm && get<0>(RangeTable170[i + 1]) >= AdjusteBtm)
					{
						IndexNear = i;
						IndexFar = i + 1;
						break;
					}
				}
			}
			
			if (CamLower == 170)
				RangeCamLower = get<1>(RangeTable170[IndexNear]) + (get<1>(RangeTable170[IndexFar]) - get<1>(RangeTable170[IndexNear]))  *  (AdjusteBtm - get<0>(RangeTable170[IndexNear])) / (get<0>(RangeTable170[IndexFar]) - get<0>(RangeTable170[IndexNear]));
			else if (CamHigher == 170)
				RangeCamHigher = get<1>(RangeTable170[IndexNear]) + (get<1>(RangeTable170[IndexFar]) - get<1>(RangeTable170[IndexNear]))  *  (AdjusteBtm - get<0>(RangeTable170[IndexNear])) / (get<0>(RangeTable170[IndexFar]) - get<0>(RangeTable170[IndexNear]));		 	
		}
	
	endof170:
		int a =1;
	} //180

    // cout<<"CamLower="<<CamLower<<endl;
    // cout<<"CamHigher="<<CamHigher<<endl;
    //cout << "RCHeigher=" << RangeCamHigher<<endl;
    //cout << "RCLower=" << RangeCamLower<<endl;
    //////////////////////////////////////////////////
    if (CameraHeight>170 || CameraHeight<140)
		Range = -1;
	else
    {
		Range = RangeCamLower + ((RangeCamHigher - RangeCamLower)*(CameraHeight - CamLower) / (CamHigher - CamLower));
	}
	// cout<<"Range="<<Range<<endl;	
	return Range;
}








