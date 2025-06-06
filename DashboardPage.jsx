import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import analyticsService from '@/services/analyticsService';

import StatsCard from '@/components/dashboard/StatsCard';
import AnalyticsChart from '@/components/dashboard/AnalyticsChart';
import RecentActivities from '@/components/dashboard/RecentActivities';
import WorkflowPerformance from '@/components/dashboard/WorkflowPerformance';
import ValueSummary from '@/components/dashboard/ValueSummary';

import { 
  Users, 
  MessageSquare, 
  Star, 
  FileText,
  Calendar
} from 'lucide-react';

const DashboardPage = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [dashboardData, setDashboardData] = useState({
    stats: {},
    charts: {},
    activities: [],
    workflows: [],
    valueSummary: {}
  });
  
  const { user } = useAuth();
  const navigate = useNavigate();
  
  // Fetch dashboard data
  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        
        // In a real app, this would be a call to the API
        // For now, we'll use mock data
        
        // Simulate API call delay
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Mock dashboard data
        const mockData = {
          stats: {
            leads: {
              value: '285',
              change: 12.5,
              changeType: 'increase',
              description: 'vs. previous period'
            },
            interactions: {
              value: '8,646',
              change: 5.2,
              changeType: 'increase',
              description: 'vs. previous period'
            },
            reviews: {
              value: '50.78',
              change: 3.1,
              changeType: 'decrease',
              description: 'vs. previous period'
            },
            content: {
              value: '216',
              change: 8.4,
              changeType: 'increase',
              description: 'vs. previous period'
            }
          },
          charts: {
            leads: {
              labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
              series: [
                {
                  name: 'New Leads',
                  data: [30, 40, 35, 50, 49, 60, 70]
                },
                {
                  name: 'Conversions',
                  data: [12, 15, 14, 22, 23, 25, 32]
                }
              ]
            },
            interactions: {
              labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
              series: [
                {
                  name: 'Emails',
                  data: [800, 1200, 1100, 1500, 1400, 1600, 1800]
                },
                {
                  name: 'SMS',
                  data: [400, 600, 550, 700, 650, 800, 900]
                }
              ]
            }
          },
          activities: [
            {
              id: 'act_1',
              type: 'lead_message',
              title: 'Lead Follow-up Email',
              description: 'Automated follow-up email sent to John Doe',
              timestamp: '2025-06-05T10:30:00Z',
              status: 'completed',
              entity: {
                type: 'Lead',
                name: 'John Doe'
              }
            },
            {
              id: 'act_2',
              type: 'review_request',
              title: 'Review Request',
              description: 'Review request sent to Sarah Smith',
              timestamp: '2025-06-05T09:45:00Z',
              status: 'completed',
              entity: {
                type: 'Customer',
                name: 'Sarah Smith'
              }
            },
            {
              id: 'act_3',
              type: 'content_generation',
              title: 'Blog Post Generated',
              description: 'New blog post "10 Tips for Small Businesses" created',
              timestamp: '2025-06-05T08:15:00Z',
              status: 'completed',
              entity: {
                type: 'Content',
                name: '10 Tips for Small Businesses'
              }
            },
            {
              id: 'act_4',
              type: 'lead_created',
              title: 'New Lead Created',
              description: 'New lead from contact form: Michael Johnson',
              timestamp: '2025-06-05T07:30:00Z',
              status: 'completed',
              entity: {
                type: 'Lead',
                name: 'Michael Johnson'
              }
            },
            {
              id: 'act_5',
              type: 'content_generation',
              title: 'Social Media Post',
              description: 'Weekly social media post generation',
              timestamp: '2025-06-04T16:45:00Z',
              status: 'failed',
              entity: {
                type: 'Content',
                name: 'Weekly Social Post'
              }
            }
          ],
          workflows: [
            {
              id: 'wf_1',
              name: 'Lead Nurturing',
              type: 'lead_nurturing',
              stats: {
                total: 120,
                successful: 108,
                failed: 12
              }
            },
            {
              id: 'wf_2',
              name: 'Review & Referral',
              type: 'review_referral',
              stats: {
                total: 85,
                successful: 72,
                failed: 13
              }
            },
            {
              id: 'wf_3',
              name: 'Content Generation',
              type: 'content_generation',
              stats: {
                total: 52,
                successful: 49,
                failed: 3
              }
            }
          ],
          valueSummary: {
            revenue: {
              total: 125000,
              monthly: 25000,
              data: [15000, 18000, 22000, 25000, 20000, 25000],
              labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
              breakdown: [
                { name: 'Lead Conv.', value: 75000 },
                { name: 'Referrals', value: 35000 },
                { name: 'Content', value: 15000 }
              ]
            },
            time: {
              total: 520,
              monthly: 104,
              data: [80, 85, 90, 85, 95, 85],
              labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
              breakdown: [
                { name: 'Lead Mgmt', value: 220 },
                { name: 'Reviews', value: 150 },
                { name: 'Content', value: 150 }
              ]
            }
          }
        };
        
        setDashboardData(mockData);
      } catch (err) {
        console.error('Error fetching dashboard data:', err);
        setError('Failed to load dashboard data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };
    
    fetchDashboardData();
  }, []);
  
  // Handle view all workflows
  const handleViewAllWorkflows = () => {
    navigate('/workflows');
  };
  
  // Show loading state
  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-muted-foreground">Loading dashboard data...</p>
        </div>
      </div>
    );
  }
  
  // Show error state
  if (error) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="rounded-full h-12 w-12 bg-rose-100 text-rose-500 flex items-center justify-center mx-auto">
            <span className="text-2xl">!</span>
          </div>
          <p className="mt-4 text-muted-foreground">{error}</p>
          <button 
            onClick={() => window.location.reload()}
            className="mt-4 text-primary hover:underline"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }
  
  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground">
          Welcome back, {user?.name || 'User'}! Here's an overview of your automation system.
        </p>
      </div>
      
      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatsCard 
          title="Total Leads" 
          value={dashboardData.stats.leads.value}
          change={dashboardData.stats.leads.change}
          changeType={dashboardData.stats.leads.changeType}
          description={dashboardData.stats.leads.description}
          icon={Users}
        />
        
        <StatsCard 
          title="Interactions" 
          value={dashboardData.stats.interactions.value}
          change={dashboardData.stats.interactions.change}
          changeType={dashboardData.stats.interactions.changeType}
          description={dashboardData.stats.interactions.description}
          icon={MessageSquare}
        />
        
        <StatsCard 
          title="Reviews" 
          value={dashboardData.stats.reviews.value}
          change={dashboardData.stats.reviews.change}
          changeType={dashboardData.stats.reviews.changeType}
          description={dashboardData.stats.reviews.description}
          icon={Star}
        />
        
        <StatsCard 
          title="Content Created" 
          value={dashboardData.stats.content.value}
          change={dashboardData.stats.content.change}
          changeType={dashboardData.stats.content.changeType}
          description={dashboardData.stats.content.description}
          icon={FileText}
        />
      </div>
      
      {/* Charts */}
      <div className="grid gap-4 md:grid-cols-2">
        <AnalyticsChart 
          title="Lead Performance" 
          data={dashboardData.charts.leads}
          type="line"
        />
        
        <AnalyticsChart 
          title="Interaction Volume" 
          data={dashboardData.charts.interactions}
          type="bar"
        />
      </div>
      
      {/* Value Summary */}
      <ValueSummary data={dashboardData.valueSummary} />
      
      {/* Workflows and Activities */}
      <div className="grid gap-4 md:grid-cols-2">
        <WorkflowPerformance 
          workflows={dashboardData.workflows}
          onViewAll={handleViewAllWorkflows}
        />
        
        <RecentActivities activities={dashboardData.activities} />
      </div>
    </div>
  );
};

export default DashboardPage;

