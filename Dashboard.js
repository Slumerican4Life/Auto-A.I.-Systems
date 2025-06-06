import React, { useState, useEffect } from 'react';
import { useQuery } from 'react-query';
import { format } from 'date-fns';
import {
  LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  PieChart, Pie, Cell
} from 'recharts';

import { fetchDashboardMetrics } from '../services/api';
import DashboardCard from '../components/dashboard/DashboardCard';
import MetricCard from '../components/dashboard/MetricCard';
import ValueSummaryCard from '../components/dashboard/ValueSummaryCard';
import ActivityFeed from '../components/dashboard/ActivityFeed';
import DateRangePicker from '../components/common/DateRangePicker';
import LoadingSpinner from '../components/common/LoadingSpinner';
import ErrorAlert from '../components/common/ErrorAlert';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

const Dashboard = () => {
  const [dateRange, setDateRange] = useState({
    startDate: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000), // 30 days ago
    endDate: new Date()
  });

  const { data, isLoading, error, refetch } = useQuery(
    ['dashboardMetrics', dateRange],
    () => fetchDashboardMetrics(dateRange.startDate, dateRange.endDate),
    {
      refetchOnWindowFocus: false,
      keepPreviousData: true
    }
  );

  useEffect(() => {
    refetch();
  }, [dateRange, refetch]);

  const handleDateRangeChange = (newRange) => {
    setDateRange(newRange);
  };

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorAlert message={error.message} />;

  const {
    summary,
    charts,
    value_summary: valueSummary,
    recent_activity: recentActivity
  } = data || {
    summary: {},
    charts: {},
    value_summary: {},
    recent_activity: []
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-800">Dashboard</h1>
        <DateRangePicker
          startDate={dateRange.startDate}
          endDate={dateRange.endDate}
          onChange={handleDateRangeChange}
        />
      </div>

      {/* Summary Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <MetricCard
          title="Leads"
          value={summary?.leads?.total || 0}
          subValue={`${summary?.leads?.conversion_rate?.toFixed(1) || 0}% Conversion`}
          trend={10}
          icon="users"
          color="blue"
        />
        <MetricCard
          title="Reviews"
          value={summary?.reviews?.completed || 0}
          subValue={`${summary?.reviews?.completion_rate?.toFixed(1) || 0}% Completion`}
          trend={5}
          icon="star"
          color="yellow"
        />
        <MetricCard
          title="Referrals"
          value={summary?.referrals?.used || 0}
          subValue={`${summary?.referrals?.usage_rate?.toFixed(1) || 0}% Usage Rate`}
          trend={-2}
          icon="share"
          color="green"
        />
        <MetricCard
          title="Content"
          value={summary?.content?.published || 0}
          subValue={`${summary?.content?.engagement?.views || 0} Views`}
          trend={15}
          icon="document"
          color="purple"
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <DashboardCard title="Lead Performance">
          <ResponsiveContainer width="100%" height={300}>
            <LineChart
              data={charts?.leads_over_time || []}
              margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="date"
                tickFormatter={(date) => format(new Date(date), 'MMM dd')}
              />
              <YAxis />
              <Tooltip
                formatter={(value, name) => [value, name === 'new' ? 'New Leads' : name === 'contacted' ? 'Contacted' : 'Converted']}
                labelFormatter={(label) => format(new Date(label), 'MMM dd, yyyy')}
              />
              <Legend />
              <Line type="monotone" dataKey="new" stroke="#0088FE" name="New Leads" />
              <Line type="monotone" dataKey="contacted" stroke="#00C49F" name="Contacted" />
              <Line type="monotone" dataKey="converted" stroke="#FFBB28" name="Converted" />
            </LineChart>
          </ResponsiveContainer>
        </DashboardCard>

        <DashboardCard title="Review Performance">
          <ResponsiveContainer width="100%" height={300}>
            <LineChart
              data={charts?.reviews_over_time || []}
              margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="date"
                tickFormatter={(date) => format(new Date(date), 'MMM dd')}
              />
              <YAxis />
              <Tooltip
                formatter={(value, name) => [value, name === 'requested' ? 'Requested' : 'Completed']}
                labelFormatter={(label) => format(new Date(label), 'MMM dd, yyyy')}
              />
              <Legend />
              <Line type="monotone" dataKey="requested" stroke="#0088FE" name="Requested" />
              <Line type="monotone" dataKey="completed" stroke="#00C49F" name="Completed" />
            </LineChart>
          </ResponsiveContainer>
        </DashboardCard>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        <DashboardCard title="Content Performance">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart
              data={charts?.content_over_time || []}
              margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="date"
                tickFormatter={(date) => format(new Date(date), 'MMM dd')}
              />
              <YAxis />
              <Tooltip
                formatter={(value, name) => [value, name === 'created' ? 'Created' : name === 'published' ? 'Published' : 'Views']}
                labelFormatter={(label) => format(new Date(label), 'MMM dd, yyyy')}
              />
              <Legend />
              <Bar dataKey="created" fill="#0088FE" name="Created" />
              <Bar dataKey="published" fill="#00C49F" name="Published" />
              <Bar dataKey="views" fill="#FFBB28" name="Views" />
            </BarChart>
          </ResponsiveContainer>
        </DashboardCard>

        <DashboardCard title="Lead Sources">
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={[
                  { name: 'Website', value: summary?.leads?.by_source?.website?.total || 0 },
                  { name: 'Facebook', value: summary?.leads?.by_source?.facebook?.total || 0 },
                  { name: 'Referral', value: summary?.leads?.by_source?.referral?.total || 0 },
                  { name: 'Other', value: summary?.leads?.by_source?.other?.total || 0 }
                ]}
                cx="50%"
                cy="50%"
                labelLine={false}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
              >
                {[
                  { name: 'Website', value: summary?.leads?.by_source?.website?.total || 0 },
                  { name: 'Facebook', value: summary?.leads?.by_source?.facebook?.total || 0 },
                  { name: 'Referral', value: summary?.leads?.by_source?.referral?.total || 0 },
                  { name: 'Other', value: summary?.leads?.by_source?.other?.total || 0 }
                ].map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip formatter={(value, name) => [value, name]} />
            </PieChart>
          </ResponsiveContainer>
        </DashboardCard>

        <ValueSummaryCard
          estimatedRevenue={valueSummary?.estimated_revenue || 0}
          hoursSaved={valueSummary?.hours_saved || 0}
          laborSavings={valueSummary?.labor_savings || 0}
          roiPercent={valueSummary?.roi_percent || 0}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <DashboardCard title="Recent Activity">
            <ActivityFeed activities={recentActivity || []} />
          </DashboardCard>
        </div>
        <DashboardCard title="Rating Distribution">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart
              data={[
                { name: '5 Stars', value: summary?.reviews?.rating_distribution?._5_star || 0 },
                { name: '4 Stars', value: summary?.reviews?.rating_distribution?._4_star || 0 },
                { name: '3 Stars', value: summary?.reviews?.rating_distribution?._3_star || 0 },
                { name: '2 Stars', value: summary?.reviews?.rating_distribution?._2_star || 0 },
                { name: '1 Star', value: summary?.reviews?.rating_distribution?._1_star || 0 }
              ]}
              layout="vertical"
              margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis dataKey="name" type="category" />
              <Tooltip />
              <Legend />
              <Bar dataKey="value" fill="#FFBB28" name="Reviews" />
            </BarChart>
          </ResponsiveContainer>
        </DashboardCard>
      </div>
    </div>
  );
};

export default Dashboard;

