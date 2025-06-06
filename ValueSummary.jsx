import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Chart } from '@/components/ui/chart';
import { DollarSign, Clock } from 'lucide-react';

const ValueSummary = ({ data }) => {
  // Format currency
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(value);
  };
  
  // Format hours
  const formatHours = (value) => {
    return `${value} hrs`;
  };
  
  // Chart options for revenue impact
  const revenueChartOptions = {
    chart: {
      type: 'area',
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
    fill: {
      type: 'gradient',
      gradient: {
        shadeIntensity: 1,
        opacityFrom: 0.7,
        opacityTo: 0.3,
        stops: [0, 90, 100],
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
    colors: ['var(--chart-1)'],
    xaxis: {
      categories: data?.revenue?.labels || [],
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
        formatter: (value) => formatCurrency(value),
      },
    },
    tooltip: {
      theme: 'dark',
      y: {
        formatter: (value) => formatCurrency(value),
      },
    },
  };
  
  // Chart options for time saved
  const timeChartOptions = {
    chart: {
      type: 'area',
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
    fill: {
      type: 'gradient',
      gradient: {
        shadeIntensity: 1,
        opacityFrom: 0.7,
        opacityTo: 0.3,
        stops: [0, 90, 100],
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
    colors: ['var(--chart-2)'],
    xaxis: {
      categories: data?.time?.labels || [],
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
        formatter: (value) => formatHours(value),
      },
    },
    tooltip: {
      theme: 'dark',
      y: {
        formatter: (value) => formatHours(value),
      },
    },
  };
  
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base font-medium">Value Summary</CardTitle>
      </CardHeader>
      
      <CardContent>
        <Tabs defaultValue="revenue">
          <TabsList className="grid grid-cols-2 mb-4">
            <TabsTrigger value="revenue">
              <DollarSign className="h-4 w-4 mr-2" />
              Revenue Impact
            </TabsTrigger>
            <TabsTrigger value="time">
              <Clock className="h-4 w-4 mr-2" />
              Time Saved
            </TabsTrigger>
          </TabsList>
          
          <TabsContent value="revenue" className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Total Revenue Impact</p>
                <h3 className="text-2xl font-bold">
                  {formatCurrency(data?.revenue?.total || 0)}
                </h3>
              </div>
              
              <div className="text-right">
                <p className="text-sm text-muted-foreground">Monthly Average</p>
                <h4 className="text-lg font-semibold">
                  {formatCurrency(data?.revenue?.monthly || 0)}
                </h4>
              </div>
            </div>
            
            <Chart
              height={200}
              options={revenueChartOptions}
              series={[{ name: 'Revenue Impact', data: data?.revenue?.data || [] }]}
              type="area"
            />
            
            <div className="grid grid-cols-3 gap-4 pt-2">
              {data?.revenue?.breakdown?.map((item, index) => (
                <div key={index} className="text-center">
                  <p className="text-xs text-muted-foreground">{item.name}</p>
                  <p className="text-sm font-medium">{formatCurrency(item.value)}</p>
                </div>
              ))}
            </div>
          </TabsContent>
          
          <TabsContent value="time" className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Total Hours Saved</p>
                <h3 className="text-2xl font-bold">
                  {formatHours(data?.time?.total || 0)}
                </h3>
              </div>
              
              <div className="text-right">
                <p className="text-sm text-muted-foreground">Monthly Average</p>
                <h4 className="text-lg font-semibold">
                  {formatHours(data?.time?.monthly || 0)}
                </h4>
              </div>
            </div>
            
            <Chart
              height={200}
              options={timeChartOptions}
              series={[{ name: 'Hours Saved', data: data?.time?.data || [] }]}
              type="area"
            />
            
            <div className="grid grid-cols-3 gap-4 pt-2">
              {data?.time?.breakdown?.map((item, index) => (
                <div key={index} className="text-center">
                  <p className="text-xs text-muted-foreground">{item.name}</p>
                  <p className="text-sm font-medium">{formatHours(item.value)}</p>
                </div>
              ))}
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
};

export default ValueSummary;

