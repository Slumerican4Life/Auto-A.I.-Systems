import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Chart } from '@/components/ui/chart';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

const AnalyticsChart = ({ 
  title, 
  data, 
  type = 'line', 
  height = 300,
  timeRanges = ['7d', '30d', '90d', 'all'],
  colors = ['var(--chart-1)', 'var(--chart-2)']
}) => {
  const [timeRange, setTimeRange] = useState(timeRanges[0]);
  
  // Filter data based on selected time range
  const filteredData = React.useMemo(() => {
    // In a real app, this would filter based on the time range
    // For now, we'll just return the original data
    return data;
  }, [data, timeRange]);
  
  // Prepare chart options
  const chartOptions = React.useMemo(() => {
    if (type === 'line') {
      return {
        chart: {
          type: 'line',
          toolbar: {
            show: false,
          },
          zoom: {
            enabled: false,
          },
        },
        stroke: {
          curve: 'smooth',
          width: 2,
        },
        grid: {
          borderColor: 'var(--border)',
          strokeDashArray: 4,
          padding: {
            top: 0,
            right: 0,
            bottom: 0,
            left: 0,
          },
        },
        colors,
        xaxis: {
          categories: filteredData.labels || [],
          axisBorder: {
            show: false,
          },
          axisTicks: {
            show: false,
          },
          labels: {
            style: {
              colors: 'var(--muted-foreground)',
              fontFamily: 'inherit',
            },
          },
        },
        yaxis: {
          labels: {
            style: {
              colors: 'var(--muted-foreground)',
              fontFamily: 'inherit',
            },
          },
        },
        tooltip: {
          theme: 'dark',
        },
      };
    } else if (type === 'bar') {
      return {
        chart: {
          type: 'bar',
          toolbar: {
            show: false,
          },
          zoom: {
            enabled: false,
          },
        },
        plotOptions: {
          bar: {
            borderRadius: 4,
            columnWidth: '60%',
          },
        },
        grid: {
          borderColor: 'var(--border)',
          strokeDashArray: 4,
          padding: {
            top: 0,
            right: 0,
            bottom: 0,
            left: 0,
          },
        },
        colors,
        xaxis: {
          categories: filteredData.labels || [],
          axisBorder: {
            show: false,
          },
          axisTicks: {
            show: false,
          },
          labels: {
            style: {
              colors: 'var(--muted-foreground)',
              fontFamily: 'inherit',
            },
          },
        },
        yaxis: {
          labels: {
            style: {
              colors: 'var(--muted-foreground)',
              fontFamily: 'inherit',
            },
          },
        },
        tooltip: {
          theme: 'dark',
        },
      };
    }
    
    return {};
  }, [type, filteredData, colors]);
  
  // Prepare chart series
  const chartSeries = React.useMemo(() => {
    return filteredData.series || [];
  }, [filteredData]);
  
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-base font-medium">{title}</CardTitle>
        <Select value={timeRange} onValueChange={setTimeRange}>
          <SelectTrigger className="h-8 w-[100px]">
            <SelectValue placeholder="Select range" />
          </SelectTrigger>
          <SelectContent>
            {timeRanges.map((range) => (
              <SelectItem key={range} value={range}>
                {range}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </CardHeader>
      <CardContent className="pt-0">
        <Chart
          height={height}
          options={chartOptions}
          series={chartSeries}
          type={type}
        />
      </CardContent>
    </Card>
  );
};

export default AnalyticsChart;

