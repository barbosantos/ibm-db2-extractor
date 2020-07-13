PACKAGE:=db2-table-extractor
VERSION=0.0.1

GCP_PROJECT=gcloud-functions-280407
REGISTRY=gcr.io/${GCP_PROJECT}
GIT_VERSION=$(shell ./git-version.sh)
REGION=europe-west1
SERVICE_ACCOUNT=cloudrunbquery@gcloud-functions-280407.iam.gserviceaccount.com
SECRET_ID=db2-credentials-rbns

build:
	gcloud builds submit --tag ${REGISTRY}/${PACKAGE}:${VERSION}-${GIT_VERSION}

deploy:
	gcloud run deploy ${PACKAGE} --image ${REGISTRY}/${PACKAGE}:${VERSION}-${GIT_VERSION} \
	--set-env-vars SECRET_ID=${SECRET_ID},GCP_PROJECT=${GCP_PROJECT} \
	--no-allow-unauthenticated --platform managed --region ${REGION} \
	--service-account ${SERVICE_ACCOUNT} \