#include "feature_calculator.h"

void eccentricities_calculator(full_object_detection shape, std::vector<double> &result)
{
//    std::vector<double> result;
    //dlib::point pts1, pts2, pts3, pts4;

    //-----upper mouth 1-----//
//    pts1 = shape.part(48);
//    pts2 = shape.part(51);
//    pts3 = shape.part(54);
//    result.push_back(eccentricity_calculator((pts3.x()-pts1.x())/2, (pts3.y()+pts1.y())/2 - pts2.y()))
    //res.append(eccentricity_calc((data[54][0]-data[48][0])/2, (data[54][1]+data[48][1])/2 - data[51][1]))
    result.push_back(eccentricity_calculator((shape.part(54).x()-shape.part(48).x())/2, (shape.part(54).y()+shape.part(48).y())/2 - shape.part(51).y()));


    //-----upper mouth 2-----//
//    pts1 = shape.part(48);
//    pts2 = shape.part(62);
//    pts3 = shape.part(54);
//    result.push_back(eccentricity_calculator((pts3.x()-pts1.x())/2, (pts3.y()+pts1.y())/2 - pts2.y()))
    //res.append(eccentricity_calc((data[54][0]-data[48][0])/2, (data[54][1]+data[48][1])/2 - data[62][1]))
    result.push_back(eccentricity_calculator((shape.part(54).x()-shape.part(48).x())/2, (shape.part(54).y()+shape.part(48).y())/2 - shape.part(62).y()));

    //-----lower mouth 1-----//
//    pts1 = shape.part(48);
//    pts2 = shape.part(66);
//    pts3 = shape.part(54);
//    result.push_back(eccentricity_calculator((pts3.x()-pts1.x())/2, (pts3.y()+pts1.y())/2 - pts2.y()))
    //res.append(eccentricity_calc((data[54][0]-data[48][0])/2, (data[54][1]+data[48][1])/2 - data[66][1]))
    result.push_back(eccentricity_calculator((shape.part(54).x()-shape.part(48).x())/2, (shape.part(54).y()+shape.part(48).y())/2 - shape.part(51).y()));

    //-----lower mouth 2-----//
//    pts1 = shape.part(48);
//    pts2 = shape.part(57);
//    pts3 = shape.part(54);
//    result.push_back(eccentricity_calculator((pts3.x()-pts1.x())/2, (pts3.y()+pts1.y())/2 - pts2.y()))
    //.append(eccentricity_calc((data[54][0]-data[48][0])/2, (data[54][1]+data[48][1])/2 - data[57][1]))
    result.push_back(eccentricity_calculator((shape.part(54).x()-shape.part(48).x())/2, (shape.part(54).y()+shape.part(48).y())/2 - shape.part(57).y()));

    //-----upper left eye-----//
//    pts1 = shape.part(36);
//    pts2 = shape.part(38);
//    pts3 = shape.part(39);
//    pts4 = shape.part(37);
//    result.push_back(eccentricity_calculator((pts3.x()-pts1.x())/2, (pts3.y()+pts1.y())/2 - (pts2.y()+pts4.y())/2))
    //res.append(eccentricity_calc((data[39][0]-data[36][0])/2, (data[39][1]+data[36][1])/2 - (data[38][1]+data[37][1])/2))
    result.push_back(eccentricity_calculator((shape.part(39).x()-shape.part(36).x())/2, (shape.part(39).y()+shape.part(36).y())/2 - (shape.part(38).y()+shape.part(37).y())/2));

    //-----lower left eye-----//
//    pts1 = shape.part(36);
//    pts2 = shape.part(41);
//    pts3 = shape.part(39);
//    pts4 = shape.part(40);
//    result.push_back(eccentricity_calculator((pts3.x()-pts1.x())/2, (pts3.y()+pts1.y())/2 - (pts2.y()+pts4.y())/2))
    //res.append(eccentricity_calc((data[39][0]-data[36][0])/2, (data[39][1]+data[36][1])/2 - (data[41][1]+data[40][1])/2))
    result.push_back(eccentricity_calculator((shape.part(39).x()-shape.part(36).x())/2, (shape.part(39).y()+shape.part(36).y())/2 - (shape.part(41).y()+shape.part(40).y())/2));


    //-----upper right eye-----//
//    pts1 = shape.part(42);
//    pts2 = shape.part(44);
//    pts3 = shape.part(45);
//    pts4 = shape.part(43);
//    result.push_back(eccentricity_calculator((pts3.x()-pts1.x())/2, (pts3.y()+pts1.y())/2 - (pts2.y()+pts4.y())/2))
    //res.append(eccentricity_calc((data[45][0]-data[42][0])/2, (data[45][1]+data[42][1])/2 - (data[44][1]+data[43][1])/2))
    result.push_back(eccentricity_calculator((shape.part(45).x()-shape.part(42).x())/2, (shape.part(45).y()+shape.part(42).y())/2 - (shape.part(44).y()+shape.part(43).y())/2));


    //-----lower right eye-----//
//    pts1 = shape.part(42);
//    pts2 = shape.part(47);
//    pts3 = shape.part(45);
//    pts4 = shape.part(46);
//    result.push_back(eccentricity_calculator((pts3.x()-pts1.x())/2, (pts3.y()+pts1.y())/2 - (pts2.y()+pts4.y())/2))
    //res.append(eccentricity_calc((data[45][0]-data[42][0])/2, (data[45][1]+data[42][1])/2 - (data[47][1]+data[46][1])/2))
    result.push_back(eccentricity_calculator((shape.part(45).x()-shape.part(42).x())/2, (shape.part(45).y()+shape.part(42).y())/2 - (shape.part(47).y()+shape.part(46).y())/2));


    //-----left eyebrown-----//
//    pts1 = shape.part(17);
//    pts2 = shape.part(19);
//    pts3 = shape.part(21);
//    result.push_back(eccentricity_calculator((pts3.x()-pts1.x())/2, (pts3.y()+pts1.y())/2 - pts2.y()))
    //res.append(eccentricity_calc((data[21][0]-data[17][0])/2, (data[21][1]+data[17][1])/2 - data[19][1]))
    result.push_back(eccentricity_calculator((shape.part(21).x()-shape.part(17).x())/2, shape.part(21).y()+shape.part(17).y())/2 - shape.part(19).y());


    //-----right eyebrown-----//
//    pts1 = shape.part(22);
//    pts2 = shape.part(24);
//    pts3 = shape.part(26);
//    result.push_back(eccentricity_calculator((pts3.x()-pts1.x())/2, (pts3.y()+pts1.y())/2 - pts2.y()))
    //res.append(eccentricity_calc((data[26][0]-data[22][0])/2, (data[26][1]+data[22][1])/2 - data[24][1]))
    result.push_back(eccentricity_calculator((shape.part(26).x()-shape.part(22).x())/2, shape.part(26).y()+shape.part(22).y())/2 - shape.part(24).y());
}

void linear_calculator(full_object_detection shape, std::vector<double> &result)
{
//    std::vector<double> result;
//    dlib::point pts1, pts2, pts3, pts4;
//    pts1 = shape.part(19)
//    pts2 = shape.part(8)
//    pts3 = shape.part(37)
//    pts4 = shape.part(27)
//    result.push_back((pts3.y()-pts1.y())/(pts2.y()-pts4.y()))
    result.push_back((shape.part(37).y()-shape.part(19).y())/(shape.part(8).y()-shape.part(27).y()));
    //res.append((data[37][1]-data[19][1])/(data[8][1]-data[27][1]))
//    pts1 = shape.part(33)
//    pts3 = shape.part(51)
//    result.push_back((pts3.y()-pts1.y())/(pts2.y()-pts4.y()))
    result.push_back((shape.part(51).y()-shape.part(33).y())/(shape.part(8).y()-shape.part(27).y()));
    //res.append((data[51][1]-data[33][1])/(data[8][1]-data[27][1]))
//    pts3 = shape.part(57)
//    result.push_back((pts3.y()-pts1.y())/(pts2.y()-pts4.y()))
    //res.append((data[57][1]-data[33][1])/(data[8][1]-data[27][1]))
    result.push_back((shape.part(57).y()-shape.part(33).y())/(shape.part(8).y()-shape.part(27).y()));
//    return result;
}

//void feature_calculator_13(full_object_detection shape, std::vector<double> &result)
//{
////    std::vector<double> result, linear;
////    result = eccentricities_calculator(shape);
////    linear = linear_calculator(shape);
//    ASSERT_EQ(result.size(),0) << "Result must be empty";
//
//    eccentricities_calculator(shape,result);
//    linear_calculator(shape,result);
//
//    ASSERT_EQ(result.size(),13) << "Feature size (13) do not match:" << result.size();
//
////    for (std::vector<double>::iterator it=linear.begin(); it!=linear.end(); ++it)
////        result.push_back(*it)
//}

//TODO: f_13[i] - neu[i] = 13
//void feature_calculator_26(full_object_detection shape, std::string path, std::vector<double> &result)
//{
////    std::vector<double> result;
////    result = feature_calculator_13(shape);
//
////    feature_calculator_13(shape,result);
//    eccentricities_calculator(shape,result);
//    linear_calculator(shape,result);
//
//    ifstream ifs(path, std::ifstream::in);
//
//    std::string line;
//    ifs >> line;
//    ifs.close();
//
//    std::vector<std::string> strs;
//    boost::split(strs,line,boost::is_any_of(","));
//
//    for (size_t i = 0; i < strs.size(); i++)
//        result.push_back(result[i] - std::stod(strs[i]));
//
//    ASSERT_EQ(result.size(),26) << "Feature size (26) do not match: " << result.size();
//}

std::vector<double> feature_calculator(full_object_detection shape,std::string path)
{
	std::vector<double> result;
    //ASSERT_EQ(result.size(),0) << "Result must be empty";
    //-----open mouth-----//
    result.push_back((shape.part(57).y()-shape.part(51).y())/(shape.part(54).x()-shape.part(48).x()));

    //-----open left eye-----//
    result.push_back((shape.part(41).y()-shape.part(37).y())/(shape.part(39).x()-shape.part(36).x()));

    //-----open right eye-----//
    result.push_back((shape.part(47).y()-shape.part(43).y())/(shape.part(45).x()-shape.part(42).x()));

    //-----distances-----//
    dlib::vector<double,2> vecaa(shape.part(54).x()-shape.part(48).x(),shape.part(54).y()-shape.part(48).y());
    double modulus_vecaa = std::sqrt(vecaa.dot(vecaa));

    dlib::vector<double,2> vecbb(shape.part(57).x()-shape.part(51).x(),shape.part(57).y()-shape.part(51).y());
    double modulus_vecbb = std::sqrt(vecbb.dot(vecbb));

    for (size_t i = 0; i < 9; i++)
    {
        dlib::vector<double,2> vec(shape.part(48).x()-shape.part(i).x(),shape.part(48).y()-shape.part(i).y());
        vec /= modulus_vecaa;
        double modulus_vec = std::sqrt(vec.dot(vec));
        double dot = vec.dot(vecaa);
        double cos_angle = dot/modulus_vec/modulus_vecaa;
        result.push_back(modulus_vec);
        result.push_back(cos_angle);
    }

    for (size_t i = 8; i < 17; i++)
    {
        dlib::vector<double,2> vec(shape.part(54).x()-shape.part(i).x(),shape.part(54).y()-shape.part(i).y());
        vec /= modulus_vecaa;
        double modulus_vec = std::sqrt(vec.dot(vec));
        double dot = vec.dot(vecaa);
        double cos_angle = dot/modulus_vec/modulus_vecaa;
        result.push_back(modulus_vec);
        result.push_back(cos_angle);
    }

    dlib::vector<double,2> a(shape.part(48));
    dlib::vector<double,2> b(shape.part(51));
    dlib::vector<double,2> nvecaa(vecaa.y(),-vecaa.x());
    dlib::vector<double,2> nvecbb(vecbb.y(),-vecbb.x());

    if (nvecbb.x() == 0 && nvecbb.y() == 0)
    {
        nvecbb.x() = 1;
        nvecbb.y() = 0;
    }

    double c = nvecaa.dot(a);
    double d = nvecbb.dot(b);

    dlib::matrix<double,2,2> f_matrix;
    f_matrix =  nvecaa.x(), nvecaa.y(),
                nvecbb.x(), nvecbb.y();

    dlib::matrix<double,2,1> free_col;
    free_col =  c,
                d;

    dlib::matrix<double> cross = dlib::inv(f_matrix)*free_col;

    for (size_t i = 48; i < 68; i++)
    {
        dlib::vector<double,2> vec(cross(0)-shape.part(i).x(),cross(1)-shape.part(i).y());
        vec /= modulus_vecaa;
        double modulus_vec = std::sqrt(vec.dot(vec));
        if (modulus_vec == 0) modulus_vec == 1;
        double dot = vec.dot(vecaa);
        double cos_angle = dot/modulus_vec/modulus_vecaa;
        result.push_back(modulus_vec);
        result.push_back(cos_angle);
    }

    //-----F_26-----//
    eccentricities_calculator(shape,result);
    linear_calculator(shape,result);

    ifstream ifs(path, std::ifstream::in);

    std::string line;
    ifs >> line;
    ifs.close();

    std::vector<std::string> strs;
    boost::split(strs,line,boost::is_any_of(","));

    for (size_t i = 0; i < strs.size(); i++)
        result.push_back(result[i] - std::stod(strs[i]));

    //EXPECT_EQ(result.size(),105) << "Feature size (105) do not match: " << result.size();
	return result;
}
