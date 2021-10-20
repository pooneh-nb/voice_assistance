#!/bin/bash

sudo cp ../avs-changes/main.cpp $1/avs-device-sdk/SampleApp/src/main.cpp
sudo cp ../avs-changes/LibcurlHTTP2Request.h $1/avs-device-sdk/AVSCommon/Utils/include/AVSCommon/Utils/LibcurlUtils/LibcurlHTTP2Request.h
sudo cp ../avs-changes/LibcurlHTTP2Request.cpp $1/avs-device-sdk/AVSCommon/Utils/src/LibcurlUtils/LibcurlHTTP2Request.cpp
