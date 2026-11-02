/**
 * Local stub mirroring crm-inbox-fe InboxService method surface.
 * Source: MyLocalCRM/repos/crm-inbox-fe/src/app/inbox/services/inbox.service.ts
 *
 * When useMock=true, loads src/assets/mock/conversations.json.
 * When false, POSTs to the same gateway paths as production inbox FE.
 */
import { Injectable } from '@angular/core';
import { Observable, from, map } from 'rxjs';
import { environment } from 'src/environments/environment';
import { MessagingApiPaths } from 'src/app/core/service/messaging-api.constants';

export interface ConversationRow {
  conversationId: string;
  candidateName: string;
  userId: string;
  channel: 'sms' | 'whatsapp' | 'email' | string;
  vendor?: string;
  lastMessage?: string;
  unreadCount?: number;
  status?: string;
  optInSms?: boolean;
  optInWhatsApp?: boolean;
  updatedAt?: string;
  phone?: string;
  email?: string;
}

@Injectable({ providedIn: 'root' })
export class InboxService {
  private endpoint = `${environment.endpoint.crmHub}/messaging-gateway-service/`;
  private facadeEndpoint = `${environment.endpoint.crmHub}/email-facade-service/`;

  /** Mirrors getCandidateList → POST .../v1.0/inbox/getConversations */
  getCandidateList(inboxListCriteria: Record<string, unknown>): Observable<{ conversations: ConversationRow[] }> {
    if (environment.useMock) {
      return from(fetch('assets/mock/conversations.json').then((r) => r.json())).pipe(
        map((body: { conversations: ConversationRow[] }) => body)
      );
    }
    const url = `${this.endpoint}v1.0/inbox/getConversations`;
    return from(
      fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(inboxListCriteria),
      }).then((r) => r.json())
    );
  }

  getConversationHistory(req: Record<string, unknown>): Observable<unknown> {
    const url = `${this.endpoint}v1.0/inbox/getCandidateChat`;
    return this.post(url, req);
  }

  getUnreadSmsCount(req: Record<string, unknown>): Observable<unknown> {
    const url = `${this.endpoint}v1.0/inbox/totalUnreadCount`;
    return this.post(url, req);
  }

  /** Convenience — documents path map for implementers */
  static paths = MessagingApiPaths;

  private post(url: string, body: unknown): Observable<unknown> {
    if (environment.useMock) {
      return from(Promise.resolve({ mock: true, url, body }));
    }
    return from(
      fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      }).then((r) => r.json())
    );
  }
}
