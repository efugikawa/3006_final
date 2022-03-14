import FP_precip_load as rain
import FP_crime_load as crime
import CO_log_setup as cls_log
from collections import defaultdict
import matplotlib.pyplot as plt

logger = cls_log.Logger_FP_BE()


def crime_eda():
    crime_data = crime.load_CO_crime_data(2010, logger)
    by_county = defaultdict(int)
    for i in range(len(crime_data)):
        by_county[crime_data.iloc[i, 3]] += 1

    sorted_by_count = dict(sorted(by_county.items(), key=lambda x: x[1], reverse=True))
    for k, v in by_county.items():
        if v < 1000:
            sorted_by_count.pop(k)

    logger.info("create crime line graph")
    plt.figure(figsize=(10, 10))
    plt.plot(sorted_by_count.keys(), sorted_by_count.values())
    plt.xticks(rotation='vertical')
    plt.title("Crime Count by County, 2010")
    plt.savefig("crime_count_by_county")

    logger.info("creat crime pie chart")
    plt.pie(sorted_by_count.values(), labels=sorted_by_count.keys(), rotatelabels=True)
    plt.title("Crime Count by County, 2010")
    plt.savefig("crime_count_by_county_pie")


def rain_eda():
    rain_data = rain.load_CO_precip_data(2010, logger)
    st_precip = defaultdict(float)
    st_count = defaultdict(int)
    st_avg_precip = {}

    for i in range(len(rain_data)):
        st_count[rain_data.iloc[i, 2]] += 1

    logger.info("create obs by station line graph")
    sorted_st_count = dict(sorted(st_count.items(), key=lambda x: x[1], reverse=True))
    for k, v in st_count.items():
        if v < 50:
            sorted_st_count.pop(k)

    plt.title("Observations by Station, 2010")
    plt.figure(figsize=(20, 10))
    plt.xticks(rotation='vertical')
    plt.plot(sorted_st_count.keys(), sorted_st_count.values())
    plt.savefig("obs_count")

    for i in range(len(rain_data)):
        st_precip[rain_data.iloc[i, 2]] += rain_data.iloc[i, 7]

    for st, total in st_precip.items():
        st_avg_precip[st] = (total / st_count[st])

    sorted_avg_precip = dict(sorted(st_avg_precip.items(), key=lambda x: x[1], reverse=True))

    for k, v in st_avg_precip.items():
        if v < 20:
            sorted_avg_precip.pop(k)

    logger.info("create avg precipitation by station line graph")
    plt.title("Average Precipitation by Station, 2010")
    plt.plot(sorted_avg_precip.keys(), sorted_avg_precip.values())
    plt.savefig("avg_precip_by_station")


crime_eda()
rain_eda()
