{{ define "chiller.pod" -}}
metadata:
  labels:
    app: {{ .name }}
  name: {{ .name }}
spec:
  {{- if .configMapVol }}
  volumes:
    {{- range .configMapVol }}
  - name: {{ .cmName }}
    configMap:
      name: {{ .cmName }}
    {{- end }}
  {{- end }}
  containers:
    {{- with .image }}
  - image: {{ .repo }}{{ .name }}{{ .tag }}
    {{- end }}
    name: {{ .name }}

    {{- if .ports }}
    ports:
      {{- range .ports }}
    - containerPort: {{ .port }}
      {{- end }}
    {{- end }}

    {{- if .configMapVol }}
    volumeMounts:
      {{- range .configMapVol }}
    - name: {{ .cmName }}
      mountPath: {{ .mountPath }}
      readOnly: true
      {{- end }}
    {{- end }}

    {{- if or .env .envSecret }}
    env:
      {{- range .env }}
    - name: {{ .env }}
      value: {{ .value }}
      {{- end }}

      {{- range .envSecret }}
    - name: {{ .env }}
      valueFrom:
        secretKeyRef:
          name: {{ .secret }}
          key: {{ .key }}
      {{- end }}
    {{- end }}

{{- end }}
