{{ define "chiller.service" -}}
apiVersion: v1
kind: Service
metadata:
  labels:
    app: {{ .name }}
  name: {{ .name }}
spec:
  selector:
    app: {{ .name }}
  {{- if .ports }}
  ports:
    {{- range .ports }}
  - port: {{ .port }}
      {{- if .name }}
    name: {{ .name }}
      {{- end }}
    {{- end }}
    {{- if .statsdExporter }}
  - port: 9102
    name: prometheus
    {{- end }}
  {{- end }}
{{- end }}
