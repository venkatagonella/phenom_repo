/**
 * Stub of InboxPageComponent — selector/route mirror of crm-inbox-fe.
 * Source: .../crm-inbox-fe/src/app/inbox/inbox-page.component.ts
 *
 * Runnable UI for this prototype is prototypes/messaging-dashboard.html (PDS HTML).
 * This TS file is the structural placeholder for a real Angular MFE port.
 */
import { Component, OnInit } from '@angular/core';
import { InboxService, ConversationRow } from '../services/inbox.service';

@Component({
  selector: 'app-inbox-page',
  templateUrl: './inbox-page.component.html',
  styleUrls: ['./inbox-page.component.scss'],
})
export class InboxPageComponent implements OnInit {
  candidateList: ConversationRow[] = [];
  loading = true;
  filterOption = {
    searchKeyword: '',
    currentTab: 'all',
    totalCount: 0,
  };

  constructor(private inboxService: InboxService) {}

  ngOnInit(): void {
    this.inboxService.getCandidateList({ currentTab: 'all' }).subscribe({
      next: (res) => {
        this.candidateList = res.conversations || [];
        this.filterOption.totalCount = this.candidateList.length;
        this.loading = false;
      },
      error: () => {
        this.loading = false;
      },
    });
  }
}
