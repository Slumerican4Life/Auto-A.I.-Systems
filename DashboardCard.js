import React from 'react';
import PropTypes from 'prop-types';

const DashboardCard = ({ title, children, className, actions }) => {
  return (
    <div className={`bg-white overflow-hidden shadow rounded-lg ${className}`}>
      <div className="px-4 py-5 sm:px-6 flex justify-between items-center">
        <h3 className="text-lg leading-6 font-medium text-gray-900">{title}</h3>
        {actions && <div className="flex space-x-2">{actions}</div>}
      </div>
      <div className="px-4 py-5 sm:p-6">{children}</div>
    </div>
  );
};

DashboardCard.propTypes = {
  title: PropTypes.string.isRequired,
  children: PropTypes.node.isRequired,
  className: PropTypes.string,
  actions: PropTypes.node,
};

DashboardCard.defaultProps = {
  className: '',
  actions: null,
};

export default DashboardCard;

