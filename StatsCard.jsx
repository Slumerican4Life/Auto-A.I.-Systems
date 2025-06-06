import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { ArrowUp, ArrowDown, Minus } from 'lucide-react';

const StatsCard = ({ title, value, change, changeType, icon: Icon, description }) => {
  // Determine change indicator
  const renderChangeIndicator = () => {
    if (changeType === 'increase') {
      return (
        <div className="flex items-center text-emerald-500">
          <ArrowUp className="h-4 w-4 mr-1" />
          <span>{change}%</span>
        </div>
      );
    } else if (changeType === 'decrease') {
      return (
        <div className="flex items-center text-rose-500">
          <ArrowDown className="h-4 w-4 mr-1" />
          <span>{change}%</span>
        </div>
      );
    } else {
      return (
        <div className="flex items-center text-muted-foreground">
          <Minus className="h-4 w-4 mr-1" />
          <span>No change</span>
        </div>
      );
    }
  };

  return (
    <Card>
      <CardContent className="p-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-muted-foreground">{title}</p>
            <h3 className="text-2xl font-bold mt-1">{value}</h3>
          </div>
          {Icon && (
            <div className="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center">
              <Icon className="h-5 w-5 text-primary" />
            </div>
          )}
        </div>
        
        <div className="flex items-center justify-between mt-4">
          {renderChangeIndicator()}
          {description && (
            <span className="text-xs text-muted-foreground">{description}</span>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default StatsCard;

