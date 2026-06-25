export type PxViewType = 'standard' | 'custom';

export interface PxViewMenuItem {
  label: string;
  leftIcon?: string;
  disabled?: boolean;
}

export interface PxViewGroupItem {
  id: string;
  label: string;
  type: PxViewType;
  badgeNumber?: number;
  subtitle?: string;
  icon?: string;
  menuItems?: PxViewMenuItem[];
  disabled?: boolean;
}

export interface PxViewMenuActionEvent {
  item: PxViewMenuItem;
  view: PxViewGroupItem;
}
