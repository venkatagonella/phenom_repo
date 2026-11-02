/**
 * API path constants grounded to crm-messaging-platform + crm-inbox-fe.
 * Cite: phenom-knowledge/messaging/routing.yaml
 */
export const MessagingApiPaths = {
  /** InboxService.getCandidateList — verified */
  getConversations: 'messaging-gateway-service/v1.0/inbox/getConversations',
  /** InboxService.getConversationHistory */
  getCandidateChat: 'messaging-gateway-service/v1.0/inbox/getCandidateChat',
  /** InboxService.getUnreadSmsCount */
  totalUnreadCount: 'messaging-gateway-service/v1.0/inbox/totalUnreadCount',
  /** InboxService.readUnreadConversation */
  changeReadConversationStatus:
    'messaging-gateway-service/v1.0/inbox/changeReadConversationStatus',
  /** InboxService.archivedConversation */
  changeArchiveConversationStatus:
    'messaging-gateway-service/v1.0/inbox/changeArchiveConversationStatus',
  /** InboxService.getSMSInboxSearch — email-facade */
  inboxSearch: 'email-facade-service/v1.0/inbox/search',
  /** Voice — VoiceCallController / UI twilio-voice.service */
  voiceToken: 'voice-call-service/api/v1/communication/token',
  /** WhatsApp campaign save — UI path; module mapping unverified */
  whatsappCampaignSave: 'messaging-campaign-service/v1.0/whatsapp/campaign/save',
  /** SMS send — UI sms.service; text-api-service SMSController on platform */
  sendSmsToCandidates: 'sms-service/sendSMSToCandidates',
} as const;
