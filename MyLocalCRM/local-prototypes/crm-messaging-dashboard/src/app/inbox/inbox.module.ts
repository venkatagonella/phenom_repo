import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { InboxPageComponent } from './inbox-page/inbox-page.component';

const routes: Routes = [
  { path: '', component: InboxPageComponent },
];

/**
 * MFE expose target (mirrors crm-inbox-fe webpack exposes './inbox').
 * Host shell would remoteEntry → InboxModule.
 */
@NgModule({
  declarations: [InboxPageComponent],
  imports: [CommonModule, RouterModule.forChild(routes)],
})
export class InboxModule {}
