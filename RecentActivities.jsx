import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { 
  MessageSquare, 
  Star, 
  FileText, 
  CheckCircle, 
  AlertCircle, 
  Clock,
  User
} from 'lucide-react';

const getActivityIcon = (type) => {
  switch (type) {
    case 'lead_message':
      return <MessageSquare className="h-4 w-4" />;
    case 'review_request':
      return <Star className="h-4 w-4" />;
    case 'content_generation':
      return <FileText className="h-4 w-4" />;
    case 'lead_created':
      return <User className="h-4 w-4" />;
    default:
      return <Clock className="h-4 w-4" />;
  }
};

const getStatusBadge = (status) => {
  switch (status) {
    case 'completed':
      return (
        <Badge variant="outline" className="bg-emerald-50 text-emerald-700 border-emerald-200">
          <CheckCircle className="h-3 w-3 mr-1" />
          Completed
        </Badge>
      );
    case 'failed':
      return (
        <Badge variant="outline" className="bg-rose-50 text-rose-700 border-rose-200">
          <AlertCircle className="h-3 w-3 mr-1" />
          Failed
        </Badge>
      );
    case 'pending':
      return (
        <Badge variant="outline" className="bg-amber-50 text-amber-700 border-amber-200">
          <Clock className="h-3 w-3 mr-1" />
          Pending
        </Badge>
      );
    default:
      return (
        <Badge variant="outline">
          {status}
        </Badge>
      );
  }
};

const formatTime = (timestamp) => {
  const date = new Date(timestamp);
  return new Intl.DateTimeFormat('en-US', {
    hour: 'numeric',
    minute: 'numeric',
    hour12: true
  }).format(date);
};

const ActivityItem = ({ activity }) => {
  return (
    <div className="flex items-start space-x-4 py-3">
      <div className="rounded-full p-2 bg-primary/10">
        {getActivityIcon(activity.type)}
      </div>
      
      <div className="flex-1 space-y-1">
        <div className="flex items-center justify-between">
          <p className="text-sm font-medium">{activity.title}</p>
          <span className="text-xs text-muted-foreground">
            {formatTime(activity.timestamp)}
          </span>
        </div>
        
        <p className="text-xs text-muted-foreground">{activity.description}</p>
        
        <div className="flex items-center pt-1">
          {getStatusBadge(activity.status)}
          
          {activity.entity && (
            <span className="text-xs text-muted-foreground ml-2">
              {activity.entity.type}: {activity.entity.name}
            </span>
          )}
        </div>
      </div>
    </div>
  );
};

const RecentActivities = ({ activities = [] }) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base font-medium">Recent Activities</CardTitle>
      </CardHeader>
      
      <CardContent className="p-0">
        <div className="divide-y divide-border">
          {activities.length > 0 ? (
            activities.map((activity) => (
              <ActivityItem key={activity.id} activity={activity} />
            ))
          ) : (
            <div className="py-6 text-center text-muted-foreground">
              No recent activities
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default RecentActivities;

