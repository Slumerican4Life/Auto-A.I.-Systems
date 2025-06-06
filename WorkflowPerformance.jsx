import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { 
  MessageSquare, 
  Star, 
  FileText,
  ArrowRight
} from 'lucide-react';

const getWorkflowIcon = (type) => {
  switch (type) {
    case 'lead_nurturing':
      return <MessageSquare className="h-5 w-5" />;
    case 'review_referral':
      return <Star className="h-5 w-5" />;
    case 'content_generation':
      return <FileText className="h-5 w-5" />;
    default:
      return null;
  }
};

const WorkflowItem = ({ workflow }) => {
  // Calculate success rate
  const successRate = workflow.stats.total > 0
    ? Math.round((workflow.stats.successful / workflow.stats.total) * 100)
    : 0;
  
  // Determine progress color
  const getProgressColor = (rate) => {
    if (rate >= 90) return 'bg-emerald-500';
    if (rate >= 70) return 'bg-amber-500';
    return 'bg-rose-500';
  };
  
  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <div className="rounded-full p-2 bg-primary/10 text-primary">
            {getWorkflowIcon(workflow.type)}
          </div>
          <div>
            <p className="text-sm font-medium">{workflow.name}</p>
            <p className="text-xs text-muted-foreground">
              {workflow.stats.total} runs • {workflow.stats.successful} successful
            </p>
          </div>
        </div>
        
        <div className="text-right">
          <p className="text-sm font-medium">{successRate}%</p>
          <p className="text-xs text-muted-foreground">Success rate</p>
        </div>
      </div>
      
      <Progress value={successRate} className={getProgressColor(successRate)} />
    </div>
  );
};

const WorkflowPerformance = ({ workflows = [], onViewAll }) => {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-base font-medium">Workflow Performance</CardTitle>
        <button 
          onClick={onViewAll}
          className="text-sm text-primary flex items-center hover:underline"
        >
          View all
          <ArrowRight className="h-4 w-4 ml-1" />
        </button>
      </CardHeader>
      
      <CardContent>
        <div className="space-y-4">
          {workflows.length > 0 ? (
            workflows.map((workflow) => (
              <WorkflowItem key={workflow.id} workflow={workflow} />
            ))
          ) : (
            <div className="py-6 text-center text-muted-foreground">
              No workflow data available
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default WorkflowPerformance;

