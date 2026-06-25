(function () {
  const params = new URLSearchParams(window.location.search);
  const jobId = params.get('jobId') ?? '';
  const userId = params.get('userId') ?? 'recruiter-demo';
  const tenantId = params.get('tenantId') ?? 'demo-tenant';

  let selectedSource = 'template';

  const headers = {
    'Content-Type': 'application/json',
    'x-user-id': userId,
    'x-tenant-id': tenantId,
  };

  const els = {
    pageTitle: document.getElementById('page-title'),
    pageSubtitle: document.getElementById('page-subtitle'),
    breadcrumb: document.getElementById('breadcrumb-current'),
    createFlow: document.getElementById('create-flow'),
    jobDetail: document.getElementById('job-detail'),
    createBtn: document.getElementById('create-btn'),
    cancelBtn: document.getElementById('cancel-btn'),
    closeBtn: document.getElementById('close-btn'),
    deleteBtn: document.getElementById('delete-btn'),
    footerHint: document.getElementById('footer-hint'),
    roleBadge: document.getElementById('role-badge'),
    roleBadgeText: document.getElementById('role-badge-text'),
    hiringTeamRoleText: document.getElementById('hiring-team-role-text'),
    jobStatusBadge: document.getElementById('job-status-badge'),
    jobIdDisplay: document.getElementById('job-id-display'),
    jobCreatedBy: document.getElementById('job-created-by'),
    jobSource: document.getElementById('job-source'),
    jobStatus: document.getElementById('job-status'),
    userAvatar: document.getElementById('user-avatar'),
    userDisplayName: document.getElementById('user-display-name'),
    toast: document.getElementById('toast'),
    createOptions: document.querySelectorAll('.create-option'),
  };

  function showToast(message, isError) {
    els.toast.textContent = message;
    els.toast.classList.toggle('pds-toast--error', !!isError);
    els.toast.classList.add('is-visible');
    setTimeout(() => els.toast.classList.remove('is-visible'), 3200);
  }

  function show(el) {
    el.classList.remove('is-hidden');
  }

  function hide(el) {
    el.classList.add('is-hidden');
  }

  function setUserDisplay() {
    const isSecondary = userId.includes('secondary');
    const initials = isSecondary ? 'SR' : 'PR';
    const name = isSecondary ? 'Alex Secondary' : 'Jordan Primary';
    els.userAvatar.textContent = initials;
    els.userDisplayName.textContent = name;
    document.getElementById('user-display-email').textContent =
      `${userId}@demo.phenom.com`;
  }

  function applyPermissions(perms) {
    const roleName = perms.effectiveRole?.displayName ?? 'Recruiter';
    els.roleBadgeText.textContent = roleName;
    els.hiringTeamRoleText.textContent = roleName;
    show(els.roleBadge);

    if (perms.canDelete) show(els.deleteBtn);
    else hide(els.deleteBtn);

    if (perms.canClose) show(els.closeBtn);
    else hide(els.closeBtn);

    if (!perms.canDelete && !perms.canClose) {
      els.footerHint.textContent =
        'As a Secondary Recruiter you can create jobs but cannot close or delete requisitions assigned to you.';
    } else {
      els.footerHint.textContent =
        'As Primary Recruiter you can manage the full job lifecycle for this requisition.';
    }
  }

  async function loadPermissions(id) {
    const res = await fetch(`/api/jobs/${id}/permissions`, { headers });
    if (!res.ok) {
      showToast('Failed to load permissions', true);
      return;
    }
    applyPermissions(await res.json());
  }

  function showExistingJobView() {
    els.pageTitle.textContent = 'Job Requisition';
    els.pageSubtitle.textContent = 'Review requisition details and manage lifecycle actions.';
    els.breadcrumb.textContent = 'Job Details';
    hide(els.createFlow);
    show(els.jobDetail);
    show(els.jobStatusBadge);
    hide(els.createBtn);
    els.cancelBtn.textContent = 'Back to Jobs';
  }

  function showCreateView() {
    els.pageTitle.textContent = 'Create New Job';
    els.pageSubtitle.textContent = 'Choose how to create a requisition and configure job details.';
    els.breadcrumb.textContent = 'Create New Job';
    show(els.createFlow);
    hide(els.jobDetail);
    hide(els.jobStatusBadge);
    hide(els.closeBtn);
    hide(els.deleteBtn);
    show(els.createBtn);
    els.cancelBtn.textContent = 'Cancel';
  }

  async function loadJobDetails(id) {
    const permsRes = await fetch(`/api/jobs/${id}/permissions`, { headers });
    if (!permsRes.ok) return;
    const perms = await permsRes.json();
    applyPermissions(perms);

    els.jobIdDisplay.value = id;
    els.jobCreatedBy.value = '—';
    els.jobSource.value = 'template';
    els.jobStatus.value = 'Open';
  }

  els.createOptions.forEach((btn) => {
    btn.addEventListener('click', () => {
      selectedSource = btn.dataset.source;
      els.createOptions.forEach((b) => {
        const selected = b === btn;
        b.classList.toggle('create-option--selected', selected);
        b.setAttribute('aria-pressed', String(selected));
      });
    });
  });

  els.createBtn.addEventListener('click', async () => {
    const body = { source: selectedSource };
    if (selectedSource === 'clone' && jobId) body.cloneFromJobId = jobId;

    const res = await fetch('/api/jobs', {
      method: 'POST',
      headers,
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      showToast(`Create failed (${res.status})`, true);
      return;
    }

    const job = await res.json();
    showToast('Job created successfully');
    const url = new URL(window.location.href);
    url.searchParams.set('jobId', job.jobId);
    window.location.href = url.toString();
  });

  els.closeBtn.addEventListener('click', async () => {
    const id = jobId || els.jobIdDisplay.value;
    const res = await fetch(`/api/jobs/${id}/close`, { method: 'POST', headers });
    if (res.ok) {
      showToast('Job closed');
      els.jobStatus.value = 'Closed';
      els.jobStatusBadge.classList.remove('pds-badge--open');
      els.jobStatusBadge.classList.add('pds-badge--closed');
      els.jobStatusBadge.innerHTML = '<span class="pds-badge__dot"></span> Closed';
    } else {
      showToast(`Close failed (${res.status})`, true);
    }
  });

  els.deleteBtn.addEventListener('click', async () => {
    const id = jobId || els.jobIdDisplay.value;
    const res = await fetch(`/api/jobs/${id}`, { method: 'DELETE', headers });
    if (res.ok) {
      showToast('Job deleted');
      setTimeout(() => { window.location.href = '/'; }, 800);
    } else {
      showToast(`Delete failed (${res.status})`, true);
    }
  });

  els.cancelBtn.addEventListener('click', () => {
    window.location.href = '/';
  });

  setUserDisplay();

  if (jobId) {
    showExistingJobView();
    loadJobDetails(jobId);
    loadPermissions(jobId);
  } else {
    showCreateView();
    fetch('/api/roles/registry', { headers })
      .then((r) => (r.ok ? r.json() : null))
      .then((data) => {
        if (!data) return;
        const isSecondary = userId.includes('secondary');
        const role = data.roles.find((r) =>
          isSecondary ? r.roleId === 'secondary-recruiter' : r.roleId === 'primary-recruiter',
        );
        if (role) {
          els.hiringTeamRoleText.textContent = role.displayName;
          els.roleBadgeText.textContent = role.displayName;
          show(els.roleBadge);
        }
      });
  }
})();
