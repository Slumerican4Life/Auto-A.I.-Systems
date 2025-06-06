import React from 'react';
import PropTypes from 'prop-types';
import { format, formatDistanceToNow } from 'date-fns';
import { 
  UserAddIcon, 
  ChatAlt2Icon, 
  StarIcon, 
  ShareIcon, 
  DocumentTextIcon,
  CheckCircleIcon,
  ExclamationCircleIcon
} from '@heroicons/react/solid';

const ActivityFeed = ({ activities }) => {
  const getIcon = (type) => {
    switch (type) {
      case 'lead_created':
      case 'lead_updated':
        return <UserAddIcon className="h-5 w-5 text-blue-500" />;
      case 'interaction_created':
        return <ChatAlt2Icon className="h-5 w-5 text-green-500" />;
      case 'review_requested':
      case 'review_completed':
        return <StarIcon className="h-5 w-5 text-yellow-500" />;
      case 'referral_created':
      case 'referral_used':
        return <ShareIcon className="h-5 w-5 text-purple-500" />;
      case 'content_created':
      case 'content_published':
        return <DocumentTextIcon className="h-5 w-5 text-indigo-500" />;
      case 'success':
        return <CheckCircleIcon className="h-5 w-5 text-green-500" />;
      case 'error':
        return <ExclamationCircleIcon className="h-5 w-5 text-red-500" />;
      default:
        return <DocumentTextIcon className="h-5 w-5 text-gray-500" />;
    }
  };

  const getActivityTitle = (activity) => {
    switch (activity.type) {
      case 'lead_created':
        return `New lead created: ${activity.data.name}`;
      case 'lead_updated':
        return `Lead updated: ${activity.data.name}`;
      case 'interaction_created':
        return `New interaction with ${activity.data.lead_name}`;
      case 'review_requested':
        return `Review requested from ${activity.data.customer_name}`;
      case 'review_completed':
        return `Review completed by ${activity.data.customer_name}`;
      case 'referral_created':
        return `Referral created for ${activity.data.customer_name}`;
      case 'referral_used':
        return `Referral used by ${activity.data.lead_name}`;
      case 'content_created':
        return `Content created: ${activity.data.title}`;
      case 'content_published':
        return `Content published: ${activity.data.title}`;
      default:
        return activity.title || 'Activity';
    }
  };

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return {
      relative: formatDistanceToNow(date, { addSuffix: true }),
      absolute: format(date, 'MMM d, yyyy h:mm a')
    };
  };

  if (!activities || activities.length === 0) {
    return (
      <div className="text-center py-4 text-gray-500">
        No recent activity
      </div>
    );
  }

  return (
    <div className="flow-root">
      <ul className="-mb-8">
        {activities.map((activity, activityIdx) => {
          const time = formatTime(activity.timestamp);
          
          return (
            <li key={activity.id || activityIdx}>
              <div className="relative pb-8">
                {activityIdx !== activities.length - 1 ? (
                  <span
                    className="absolute top-5 left-5 -ml-px h-full w-0.5 bg-gray-200"
                    aria-hidden="true"
                  />
                ) : null}
                <div className="relative flex items-start space-x-3">
                  <div className="relative">
                    <div className="h-10 w-10 rounded-full bg-gray-100 flex items-center justify-center ring-8 ring-white">
                      {getIcon(activity.type)}
                    </div>
                  </div>
                  <div className="min-w-0 flex-1">
                    <div>
                      <div className="text-sm">
                        <span className="font-medium text-gray-900">
                          {getActivityTitle(activity)}
                        </span>
                      </div>
                      <p className="mt-0.5 text-sm text-gray-500">
                        {activity.description}
                      </p>
                      <p className="mt-0.5 text-xs text-gray-400" title={time.absolute}>
                        {time.relative}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
};

ActivityFeed.propTypes = {
  activities: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string,
      type: PropTypes.string.isRequired,
      title: PropTypes.string,
      description: PropTypes.string,
      timestamp: PropTypes.string.isRequired,
      data: PropTypes.object,
    })
  ).isRequired,
};

export default ActivityFeed;

