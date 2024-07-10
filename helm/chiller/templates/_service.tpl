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
    {{- end }}
  {{- end }}
{{- end }}
