import { CommonModule } from '@angular/common';
import {
  Component,
  EventEmitter,
  Input,
  Output,
  booleanAttribute,
} from '@angular/core';
import { PxViewMenuItem, PxViewType } from '../models/px-view.models';

@Component({
  selector: 'px-view',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './px-view.component.html',
  styleUrl: './px-view.component.scss',
})
export class PxViewComponent {
  @Input({ required: true }) label = '';
  @Input() type: PxViewType = 'standard';
  @Input() badgeNumber?: number;
  @Input() subtitle?: string;
  @Input() icon?: string;
  @Input() menuItems: PxViewMenuItem[] = [];
  @Input({ transform: booleanAttribute }) disabled = false;
  @Input({ transform: booleanAttribute }) selected = false;
  @Input() variant: 'default' | 'pipeline' = 'default';

  @Output() viewClick = new EventEmitter<void>();
  @Output() menuShow = new EventEmitter<void>();
  @Output() menuHide = new EventEmitter<void>();
  @Output() menuItemClick = new EventEmitter<PxViewMenuItem>();

  showMenu = false;

  onViewClick(): void {
    if (this.disabled) {
      return;
    }
    this.viewClick.emit();
  }

  toggleMenu(event: Event): void {
    event.stopPropagation();
    if (this.disabled || !this.menuItems.length) {
      return;
    }
    this.showMenu = !this.showMenu;
    if (this.showMenu) {
      this.menuShow.emit();
    } else {
      this.menuHide.emit();
    }
  }

  onMenuItemClick(item: PxViewMenuItem, event: Event): void {
    event.stopPropagation();
    this.showMenu = false;
    this.menuHide.emit();
    this.menuItemClick.emit(item);
  }
}
