import React from 'react';
import PropTypes from 'prop-types';
import { CurrencyDollarIcon, ClockIcon, TrendingUpIcon } from '@heroicons/react/outline';
import DashboardCard from './DashboardCard';

const ValueSummaryCard = ({ estimatedRevenue, hoursSaved, laborSavings, roiPercent }) => {
  // Format currency
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  return (
    <DashboardCard title="Value Summary">
      <div className="space-y-5">
        <div className="flex items-center">
          <div className="flex-shrink-0 rounded-md p-2 bg-green-100">
            <CurrencyDollarIcon className="h-5 w-5 text-green-600" />
          </div>
          <div className="ml-3">
            <div className="text-sm font-medium text-gray-500">Estimated Revenue Impact</div>
            <div className="text-lg font-semibold text-gray-900">{formatCurrency(estimatedRevenue)}</div>
          </div>
        </div>

        <div className="flex items-center">
          <div className="flex-shrink-0 rounded-md p-2 bg-blue-100">
            <ClockIcon className="h-5 w-5 text-blue-600" />
          </div>
          <div className="ml-3">
            <div className="text-sm font-medium text-gray-500">Hours Saved</div>
            <div className="text-lg font-semibold text-gray-900">
              {hoursSaved.toFixed(0)} hours
              <span className="text-sm text-gray-500 ml-1">
                ({formatCurrency(laborSavings)} labor savings)
              </span>
            </div>
          </div>
        </div>

        <div className="flex items-center">
          <div className="flex-shrink-0 rounded-md p-2 bg-purple-100">
            <TrendingUpIcon className="h-5 w-5 text-purple-600" />
          </div>
          <div className="ml-3">
            <div className="text-sm font-medium text-gray-500">ROI</div>
            <div className="text-lg font-semibold text-gray-900">{roiPercent.toFixed(0)}%</div>
          </div>
        </div>

        <div className="mt-4 pt-4 border-t border-gray-200">
          <div className="text-sm text-gray-500">
            Based on your current usage and industry benchmarks
          </div>
        </div>
      </div>
    </DashboardCard>
  );
};

ValueSummaryCard.propTypes = {
  estimatedRevenue: PropTypes.number.isRequired,
  hoursSaved: PropTypes.number.isRequired,
  laborSavings: PropTypes.number.isRequired,
  roiPercent: PropTypes.number.isRequired,
};

export default ValueSummaryCard;

