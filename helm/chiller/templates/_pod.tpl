{{ define "chiller.pod" -}}
{{ $context := index . 0 -}}
{{ $appTag := index . 1 -}}
{{ with $context }}
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
      {{- $tag := ( .useAppTag | ternary $appTag .tag) }}
  - image: {{ .repo }}{{ .name }}{{ empty $tag | ternary "" ":"}}{{ $tag }}
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
  {{- if .statsdExporter }}
  initContainers:
  - name: statsd-exporter
    restartPolicy: Always
    image: prom/statsd-exporter
    args:
    - "--statsd.mapping-config=/statsd/statsd.conf"
    ports:
    - containerPort: 9102
  
    {{- if .configMapVol }}
    volumeMounts:
      {{- range .configMapVol }}
    - name: {{ .cmName }}
      mountPath: {{ .mountPath }}
      readOnly: true
      {{- end }}
    {{- end }}
  {{- end }}

{{- end }}
{{- end }}
