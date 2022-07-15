const QuorumLightNodeSDK = require('quorum-light-node-sdk');


(async() => {
    try {
        const result = await QuorumLightNodeSDK.utils.signTrx({
            groupId:  process.argv[2],
            object: {
                type:"Note",
                content: process.argv[5],
            },
            privateKey:  process.argv[3],
            aesKey:  process.argv[4],
        });
        console.log(result);
    } catch (err) {
        console.log(err);
    }
})();
