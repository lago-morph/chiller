{{ define "servicemonitor.crd" -}}
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  labels:
    name: {{ .app }}-{{ .component }}
  name: {{ .app }}-{{ .component }}
spec:
  endpoints:
  - interval: 15s
    port: prometheus
  selector:
    matchLabels:
      app: {{ .app }}-{{ .component }}
{{ end }}
