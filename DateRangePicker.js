import React, { useState, useRef, useEffect } from 'react';
import PropTypes from 'prop-types';
import { format, subDays, subMonths } from 'date-fns';
import { CalendarIcon, ChevronDownIcon } from '@heroicons/react/outline';

const DateRangePicker = ({ startDate, endDate, onChange }) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handlePresetSelect = (preset) => {
    const now = new Date();
    let newStartDate;
    let newEndDate = now;

    switch (preset) {
      case 'today':
        newStartDate = now;
        break;
      case 'yesterday':
        newStartDate = subDays(now, 1);
        newEndDate = subDays(now, 1);
        break;
      case 'last7days':
        newStartDate = subDays(now, 6);
        break;
      case 'last30days':
        newStartDate = subDays(now, 29);
        break;
      case 'thisMonth':
        newStartDate = new Date(now.getFullYear(), now.getMonth(), 1);
        break;
      case 'lastMonth':
        newStartDate = new Date(now.getFullYear(), now.getMonth() - 1, 1);
        newEndDate = new Date(now.getFullYear(), now.getMonth(), 0);
        break;
      case 'last3months':
        newStartDate = subMonths(now, 3);
        break;
      case 'last6months':
        newStartDate = subMonths(now, 6);
        break;
      default:
        newStartDate = subDays(now, 29);
    }

    onChange({ startDate: newStartDate, endDate: newEndDate });
    setIsOpen(false);
  };

  const formatDateRange = () => {
    if (!startDate || !endDate) {
      return 'Select date range';
    }

    const start = format(new Date(startDate), 'MMM d, yyyy');
    const end = format(new Date(endDate), 'MMM d, yyyy');

    if (start === end) {
      return start;
    }

    return `${start} - ${end}`;
  };

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        type="button"
        className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        onClick={() => setIsOpen(!isOpen)}
      >
        <CalendarIcon className="h-5 w-5 text-gray-400 mr-2" />
        {formatDateRange()}
        <ChevronDownIcon className="h-5 w-5 text-gray-400 ml-2" />
      </button>

      {isOpen && (
        <div className="origin-top-right absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-10">
          <div className="py-1">
            <button
              type="button"
              className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              onClick={() => handlePresetSelect('today')}
            >
              Today
            </button>
            <button
              type="button"
              className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              onClick={() => handlePresetSelect('yesterday')}
            >
              Yesterday
            </button>
            <button
              type="button"
              className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              onClick={() => handlePresetSelect('last7days')}
            >
              Last 7 days
            </button>
            <button
              type="button"
              className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              onClick={() => handlePresetSelect('last30days')}
            >
              Last 30 days
            </button>
            <button
              type="button"
              className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              onClick={() => handlePresetSelect('thisMonth')}
            >
              This month
            </button>
            <button
              type="button"
              className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              onClick={() => handlePresetSelect('lastMonth')}
            >
              Last month
            </button>
            <button
              type="button"
              className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              onClick={() => handlePresetSelect('last3months')}
            >
              Last 3 months
            </button>
            <button
              type="button"
              className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              onClick={() => handlePresetSelect('last6months')}
            >
              Last 6 months
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

DateRangePicker.propTypes = {
  startDate: PropTypes.instanceOf(Date).isRequired,
  endDate: PropTypes.instanceOf(Date).isRequired,
  onChange: PropTypes.func.isRequired,
};

export default DateRangePicker;

