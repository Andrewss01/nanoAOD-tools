#!/bin/bash
PROXY="/tmp/x509up_u180940"
CAPATH="/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates"
BASE="davs://webdav.recas.ba.infn.it:8443/cms/store/user/apuglia/TROTA_2024/PostProcessed_samples/QCD_HT40to70_2024"
davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE"