import React from 'react';
import PropTypes from 'prop-types';
import { 
  ArrowUpIcon, 
  ArrowDownIcon, 
  UsersIcon, 
  StarIcon, 
  ShareIcon, 
  DocumentTextIcon, 
  ChartBarIcon 
} from '@heroicons/react/solid';

const MetricCard = ({ title, value, subValue, trend, icon, color }) => {
  const getIcon = () => {
    switch (icon) {
      case 'users':
        return <UsersIcon className="h-6 w-6" />;
      case 'star':
        return <StarIcon className="h-6 w-6" />;
      case 'share':
        return <ShareIcon className="h-6 w-6" />;
      case 'document':
        return <DocumentTextIcon className="h-6 w-6" />;
      case 'chart':
        return <ChartBarIcon className="h-6 w-6" />;
      default:
        return <ChartBarIcon className="h-6 w-6" />;
    }
  };

  const getColorClasses = () => {
    switch (color) {
      case 'blue':
        return {
          bg: 'bg-blue-500',
          text: 'text-blue-500',
          light: 'bg-blue-100',
        };
      case 'green':
        return {
          bg: 'bg-green-500',
          text: 'text-green-500',
          light: 'bg-green-100',
        };
      case 'yellow':
        return {
          bg: 'bg-yellow-500',
          text: 'text-yellow-500',
          light: 'bg-yellow-100',
        };
      case 'red':
        return {
          bg: 'bg-red-500',
          text: 'text-red-500',
          light: 'bg-red-100',
        };
      case 'purple':
        return {
          bg: 'bg-purple-500',
          text: 'text-purple-500',
          light: 'bg-purple-100',
        };
      default:
        return {
          bg: 'bg-blue-500',
          text: 'text-blue-500',
          light: 'bg-blue-100',
        };
    }
  };

  const colorClasses = getColorClasses();

  return (
    <div className="bg-white overflow-hidden shadow rounded-lg">
      <div className="p-5">
        <div className="flex items-center">
          <div className={`flex-shrink-0 rounded-md p-3 ${colorClasses.light}`}>
            <div className={colorClasses.text}>{getIcon()}</div>
          </div>
          <div className="ml-5 w-0 flex-1">
            <dl>
              <dt className="text-sm font-medium text-gray-500 truncate">{title}</dt>
              <dd>
                <div className="text-lg font-medium text-gray-900">{value}</div>
              </dd>
            </dl>
          </div>
        </div>
      </div>
      <div className="bg-gray-50 px-5 py-3">
        <div className="flex items-center justify-between">
          <div className="text-sm text-gray-500">{subValue}</div>
          {trend !== null && (
            <div className={`flex items-center text-sm ${trend >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              {trend >= 0 ? (
                <ArrowUpIcon className="h-4 w-4 mr-1" />
              ) : (
                <ArrowDownIcon className="h-4 w-4 mr-1" />
              )}
              <span>{Math.abs(trend)}%</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

MetricCard.propTypes = {
  title: PropTypes.string.isRequired,
  value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
  subValue: PropTypes.string,
  trend: PropTypes.number,
  icon: PropTypes.oneOf(['users', 'star', 'share', 'document', 'chart']),
  color: PropTypes.oneOf(['blue', 'green', 'yellow', 'red', 'purple']),
};

MetricCard.defaultProps = {
  subValue: '',
  trend: null,
  icon: 'chart',
  color: 'blue',
};

export default MetricCard;

