import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { Sidebar, SidebarSection, SidebarItem } from '@/components/ui/sidebar';
import { 
  LayoutDashboard, 
  Users, 
  MessageSquare, 
  Star, 
  FileText, 
  Settings, 
  LogOut,
  Menu,
  X
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useMediaQuery } from '@/hooks/use-media-query';

const MainLayout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const isDesktop = useMediaQuery("(min-width: 1024px)");

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <div className="flex h-screen bg-background">
      {/* Mobile sidebar toggle */}
      <div className="fixed top-4 left-4 z-50 lg:hidden">
        <Button 
          variant="outline" 
          size="icon" 
          onClick={toggleSidebar}
          className="rounded-full shadow-md"
        >
          {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
        </Button>
      </div>

      {/* Sidebar */}
      <Sidebar 
        className={`${isDesktop ? 'block' : sidebarOpen ? 'block' : 'hidden'} 
                   fixed lg:relative z-40 h-full transition-all duration-300 ease-in-out`}
        defaultCollapsed={!isDesktop}
      >
        <SidebarSection>
          <div className="flex items-center px-4 py-2">
            <div className="flex items-center gap-2">
              <div className="h-8 w-8 rounded-full bg-primary flex items-center justify-center text-primary-foreground font-bold">
                BA
              </div>
              <div className="font-semibold text-lg">Business Automation</div>
            </div>
          </div>
        </SidebarSection>

        <SidebarSection className="flex-1">
          <SidebarItem href="/dashboard" icon={<LayoutDashboard size={20} />}>
            Dashboard
          </SidebarItem>
          <SidebarItem href="/workflows/lead-nurturing" icon={<Users size={20} />}>
            Lead Nurturing
          </SidebarItem>
          <SidebarItem href="/workflows/review-referral" icon={<Star size={20} />}>
            Reviews & Referrals
          </SidebarItem>
          <SidebarItem href="/workflows/content-generation" icon={<FileText size={20} />}>
            Content Generation
          </SidebarItem>
          <SidebarItem href="/settings" icon={<Settings size={20} />}>
            Settings
          </SidebarItem>
        </SidebarSection>

        <SidebarSection>
          <SidebarItem href="/auth/logout" icon={<LogOut size={20} />}>
            Logout
          </SidebarItem>
        </SidebarSection>
      </Sidebar>

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Main content area */}
        <main className="flex-1 overflow-y-auto p-4 md:p-6 lg:p-8">
          <Outlet />
        </main>
      </div>

      {/* Mobile sidebar overlay */}
      {!isDesktop && sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-30"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  );
};

export default MainLayout;

