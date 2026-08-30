FROM python:3.13-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
COPY examples ./examples
RUN pip install --no-cache-dir .
USER 65532:65532
EXPOSE 8080
ENTRYPOINT ["tokensre-gateway"]
CMD ["examples/multi-cloud-model-routing/45b-tokens.json", "--host", "0.0.0.0", "--port", "8080"]
