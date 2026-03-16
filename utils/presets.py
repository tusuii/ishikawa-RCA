DEVOPS_PRESETS = {
    "K8s Pod CrashLoopBackOff": {
        "effect":   "Pod CrashLoopBackOff in Production",
        "severity": "P1 - Critical",
        "service":  "api-gateway",
        "causes": {
            "People": [
                "Missing readiness probe review",
                "No runbook followed",
                "On-call engineer not notified in time",
            ],
            "Process": [
                "No canary deployment policy",
                "Missing pre-deploy smoke tests",
                "PR merged without staging validation",
            ],
            "Tools / Technology": [
                "OOMKilled — memory limit too low",
                "Broken liveness probe path",
                "Wrong container image tag (latest)",
                "containerd pull failed — insecure registry",
            ],
            "Environment": [
                "Node out of memory",
                "Network policy blocking health check",
                "NFS volume mount timeout",
            ],
            "Measurement": [
                "No alerting on restartCount > 3",
                "Grafana dashboard not reviewed",
            ],
            "Materials / Data": [
                "Missing ConfigMap key",
                "Secret not injected correctly",
            ],
        },
    },
    "Jenkins Pipeline Failure": {
        "effect":   "CI/CD Pipeline Broken — Deploy Blocked",
        "severity": "P2 - High",
        "service":  "Jenkins",
        "causes": {
            "People":             ["No pipeline owner defined", "Docs not updated after refactor"],
            "Process":            ["No rollback step defined", "Approvals stage skipped"],
            "Tools / Technology": [
                "SonarQube quality gate thresholds too strict",
                "Trivy CVE false positive blocking build",
                "Harbor push auth expired",
                "ArgoCD sync not triggered after push",
            ],
            "Environment":        [
                "Jenkins agent out of disk space",
                "Static agent sidecar misconfigured",
            ],
            "Measurement":        ["Build time SLO breached", "No flaky test tracking"],
            "Materials / Data":   ["Stale Jenkinsfile in feature branch"],
        },
    },
    "ArgoCD Sync Failure": {
        "effect":   "ArgoCD App Out-Of-Sync — Rollout Halted",
        "severity": "P2 - High",
        "service":  "ArgoCD",
        "causes": {
            "People":             ["Manifest edited directly in cluster (drift)", "No GitOps training"],
            "Process":            ["Kustomize overlay not committed", "Branch protection bypass"],
            "Tools / Technology": [
                "RBAC missing for ArgoCD service account",
                "CRD version mismatch",
                "Resource hook failed on pre-sync job",
            ],
            "Environment":        ["Git repo unreachable", "Webhook misconfigured"],
            "Measurement":        ["No sync health check alert", "Degraded app ignored"],
            "Materials / Data":   ["Wrong targetRevision in Application manifest"],
        },
    },
    "Database Connection Exhaustion": {
        "effect":   "PostgreSQL Connection Pool Exhausted",
        "severity": "P1 - Critical",
        "service":  "PostgreSQL / PgBouncer",
        "causes": {
            "People":             ["No connection pool configured", "Long-running query not killed"],
            "Process":            ["No connection limit policy in app config", "No DR runbook"],
            "Tools / Technology": [
                "PgBouncer not deployed",
                "max_connections set too low",
                "App leaking connections — missing finally block",
            ],
            "Environment":        ["High traffic spike — no HPA", "Node network saturation"],
            "Measurement":        ["No pg_stat_activity alert", "Slow query log not enabled"],
            "Materials / Data":   ["Unindexed query causing full table scan"],
        },
    },
}
