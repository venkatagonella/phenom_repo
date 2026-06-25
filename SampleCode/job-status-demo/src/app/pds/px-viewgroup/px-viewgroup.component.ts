import { CommonModule } from '@angular/common';
import {
  Component,
  EventEmitter,
  Input,
  OnChanges,
  Output,
  booleanAttribute,
} from '@angular/core';
import {
  PxViewGroupItem,
  PxViewMenuActionEvent,
  PxViewMenuItem,
} from '../models/px-view.models';
import { PxViewComponent } from '../px-view/px-view.component';

@Component({
  selector: 'px-viewgroup',
  standalone: true,
  imports: [CommonModule, PxViewComponent],
  templateUrl: './px-viewgroup.component.html',
  styleUrl: './px-viewgroup.component.scss',
})
export class PxViewGroupComponent implements OnChanges {
  @Input({ required: true }) views: PxViewGroupItem[] = [];
  @Input() selectedViewId = '';
  @Input({ transform: booleanAttribute }) showAddButton = false;
  @Input({ transform: booleanAttribute }) showSettingsButton = false;
  @Input() moreViewLabel = 'Show {} more views';
  @Input() variant: 'default' | 'pipeline' = 'default';
  @Input() showArrows = false;
  @Input() arrowBeforeIds: string[] = [];

  @Output() viewClick = new EventEmitter<PxViewGroupItem>();
  @Output() addClick = new EventEmitter<void>();
  @Output() settingsClick = new EventEmitter<void>();
  @Output() menuShow = new EventEmitter<PxViewGroupItem>();
  @Output() menuHide = new EventEmitter<PxViewGroupItem>();
  @Output() menuItemClick = new EventEmitter<PxViewMenuActionEvent>();

  visibleViews = this.views;
  overflowViews: PxViewGroupItem[] = [];

  ngOnChanges(): void {
    this.visibleViews = this.views;
    this.overflowViews = [];
  }

  isSelected(view: PxViewGroupItem): boolean {
    return view.id === this.selectedViewId;
  }

  onViewClick(view: PxViewGroupItem): void {
    this.viewClick.emit(view);
  }

  onMenuShow(view: PxViewGroupItem): void {
    this.menuShow.emit(view);
  }

  onMenuHide(view: PxViewGroupItem): void {
    this.menuHide.emit(view);
  }

  onMenuItemClick(view: PxViewGroupItem, item: PxViewMenuItem): void {
    this.menuItemClick.emit({ view, item });
  }

  shouldShowArrowAfter(view: PxViewGroupItem, index: number): boolean {
    if (!this.showArrows || index >= this.visibleViews.length - 1) {
      return false;
    }

    const nextView = this.visibleViews[index + 1];
    if (this.arrowBeforeIds.length) {
      return this.arrowBeforeIds.includes(nextView.id);
    }

    return true;
  }
}
